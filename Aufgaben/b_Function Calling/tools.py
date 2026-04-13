from datetime import datetime

def calculate_duration(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
    delta = end_date-start_date
    return delta.days

# add a function that returns the cost, assuming each night costs 100