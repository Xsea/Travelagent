from datetime import datetime
from pathlib import Path
import struct

try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

import sqlite_vec
from openai import AzureOpenAI

DB_PATH = Path(__file__).resolve().parent.parent.parent / "travel.db"

con = sqlite3.connect(DB_PATH)
con.enable_load_extension(True)
sqlite_vec.load(con)
con.enable_load_extension(False)

client = AzureOpenAI()

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
# 1. Vectorize the incoming user chat message using the embeddings API
#    and pack the result with struct.pack(f"{len(embedding)}f", *embedding)
# 2. Use the packed vector to search the space_travel_vectors table
#    with: WHERE embedding MATCH ? ORDER BY distance LIMIT 5
# 3. Use the file names to which the chunks belong, and return the text as context to the llm
