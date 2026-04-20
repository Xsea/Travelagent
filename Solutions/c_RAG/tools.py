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

# this method vectorizes user requests with the same vectorizer that was used to store all text files
def vectorize_user_request(user_request):
    embedding = client.embeddings.create(input=[user_request], model="text-embedding-3-large").data[0].embedding
    return struct.pack(f"{len(embedding)}f", *embedding)

# this method uses sqlite-vec to find the 5 closest matching chunks, and return the corresponding texts
def retrieve_closest_texts(packed_vector):
    rows = con.execute(
        """
        SELECT name FROM space_travel_vectors
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT 5
        """,
        (packed_vector,),
    ).fetchall()
    seen = set()
    texts = []
    for (file_path,) in rows:
        if file_path in seen:
            continue
        seen.add(file_path)
        with open(Path(__file__).resolve().parent.parent.parent / file_path, "r") as f:
            texts.append(f.read())
    return texts

def give_tourist_information_space(user_request):
    # vectorize user request
    packed = vectorize_user_request(user_request)
    # retrieve the closest texts
    texts = retrieve_closest_texts(packed)
    return texts
