from datetime import datetime
from openai import OpenAI
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

client = OpenAI()

def calculate_duration(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
    delta = end_date-start_date
    return delta.days

def calculate_hotel_cost(start_date, end_date):
    number_of_days = calculate_duration(start_date, end_date)
    return number_of_days * 100

# add a method that returns texts with travel information about far distant locations
# for this method you need three parts:
# 1. Vectorize the incoming user chat message
# 2. Use the vector to search the vectorDB for the closest chunks
# 3. Use the file names to which the chunks belong, and return the text as context to the llm
