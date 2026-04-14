from datetime import datetime


def calculate_duration(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
    delta = end_date - start_date
    return delta.days


def calculate_hotel_cost(start_date, end_date):
    number_of_days = calculate_duration(start_date, end_date)
    return number_of_days * 100

# Add a method that returns texts with travel information about far distant locations.
# You'll need three steps:
#   1. Vectorize the incoming user chat message
#   2. Use the vector to search travel.db (sqlite-vec) for the closest chunks
#   3. Read the matching files and return their text as context for the LLM
#
# Helpers are already implemented for you in hints.py — feel free to use them.
