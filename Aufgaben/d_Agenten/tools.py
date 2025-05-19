from datetime import datetime
from pathlib import Path

from openai import AzureOpenAI
import psycopg2
import sqlite3

db_params = {
    'dbname': 'vectorDB',
    'user': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': 5432
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

con = sqlite3.connect(Path(__file__) / ".." / ".." / ".." / "travel.db")
cur = con.cursor()


client = AzureOpenAI()

def calculate_duration(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
    delta = end_date-start_date
    return delta.days

def calculate_hotel_cost(start_date, end_date, price):
    number_of_days = calculate_duration(start_date, end_date)
    return number_of_days * price

# this method vectorizes user requests with the same vectorizer that was used to store all text files
def vectorize_user_request(user_request):
    return client.embeddings.create(input=[user_request], model="text-embedding-3-large").data[0].embedding

# this method uses an SQL request on the pgvector database
# using the cosine distance, we find the 5 closest matching chunks, and return the corresponding texts
# you can play around here for very different results
def retrieve_closest_texts(vector):
    texts = []
    select_query = f"SELECT * FROM space_travel_vectors ORDER BY vector_column <=> '{vector}' LIMIT 5;"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    # return the texts of the files
    named_files = []
    for row in rows:
        named_files.append(row[1])
    for file in set(named_files):
        with open(file, 'r') as f:
            texts.append(f.read())
    return texts

def give_tourist_information_space(user_request):
    # vectorize user request
    vector = vectorize_user_request(user_request)
    # retrieve the closest texts
    texts = retrieve_closest_texts(vector)
    result = ""
    for text in texts:
        result += f"Text: {text} \n"
    return result

def list_hotels(location):
    result = cur.execute("SELECT name FROM hotels WHERE location = ?", (location,))
    rows = result.fetchall()
    hotel_names = ""
    for row in rows:
        hotel_names += row[0] + ", "
    return hotel_names[:-2]

def get_hotel_availabilities(hotel_name):
    availabilities = cur.execute("SELECT start, end FROM availabilities WHERE name = ?", (hotel_name,))
    availability_rows = availabilities.fetchall()
    if len(availability_rows) == 0:
        raise Exception("Hotel does not exist")
    return availability_rows

def give_hotel_information(hotel_name):
    details = cur.execute("SELECT descriptionFile, price FROM hotels WHERE name = ?", (hotel_name,))
    detail_rows = details.fetchall()
    availability_rows = get_hotel_availabilities(hotel_name)
    availability_string = ""
    for row in availability_rows:
        availability_string += f"from: {row[0]}, to: {row[1]} and "

    return f"hotel costs: {detail_rows[0][1]}, hotel availabilities: {availability_string[:-4]}"

def collect_information_from_the_user(question_to_ask):
    response = str(input(question_to_ask + "\n"))
    return response

def book_flights(arrival_port, outbound_date, return_date):
    if arrival_port not in ["Luna", "Mars", "Massage"]:
        raise Exception("Arrival port does not exist!")

    out_date = datetime.strptime(outbound_date, '%Y-%m-%d')
    return_date = datetime.strptime(return_date,'%Y-%m-%d')
    if out_date > return_date:
        raise Exception("Outbound date is after return date")

    return f"Flight booked to {arrival_port} on the {outbound_date}, flight home booked for the {return_date}"

def book_hotel(hotel_name, check_in, check_out):
    check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
    check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
    if check_in_date > check_out_date:
        raise Exception("Check in date is after check out date")

    availabilities = get_hotel_availabilities(hotel_name)
    is_room_available = False
    for availability in availabilities:
        start_available = datetime.strptime(availability[0].split(" ")[0], '%Y-%m-%d')
        end_available = datetime.strptime(availability[1].split(" ")[0], '%Y-%m-%d')
        if start_available <= check_in_date and end_available >= check_out_date:
            is_room_available = True

    if not is_room_available:
        raise Exception("No room available")

    price_row = cur.execute("SELECT price FROM hotels WHERE name = ?", (hotel_name,))
    price = price_row.fetchone()
    cost = calculate_hotel_cost(check_in, check_out, price[0])
    return f"The hotel {hotel_name} was booked from {check_in} until {check_out} it will cost you {cost}€"
