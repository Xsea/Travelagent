from datetime import datetime
from openai import AzureOpenAI
import psycopg2

db_params = {
    'dbname': 'vectorDB',
    'user': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': 5432
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()


client = AzureOpenAI()

def calculate_duration(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
    delta = end_date-start_date
    return delta.days

def calculate_hotel_cost(start_date, end_date):
    number_of_days = calculate_duration(start_date, end_date)
    return number_of_days * 100

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
        # check if you need to adapt paths when using the solution
        file = "../../" + file
        with open(file, 'r') as f:
            texts.append(f.read())
    return texts

def give_tourist_information_space(user_request):
    # vectorize user request
    vector = vectorize_user_request(user_request)
    # retrieve the closest texts
    texts = retrieve_closest_texts(vector)
    return texts