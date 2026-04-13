import sqlite3
import struct
from datetime import datetime
from pathlib import Path

import sqlite_vec
from openai import AzureOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "travel.db"

con = sqlite3.connect(DB_PATH)
con.enable_load_extension(True)
sqlite_vec.load(con)
con.enable_load_extension(False)

client = AzureOpenAI()


def calculate_duration(start_date_string, end_date_string):
    start_date = datetime.strptime(start_date_string, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_string, "%Y-%m-%d")
    delta = end_date - start_date
    return delta.days


def calculate_hotel_cost(start_date, end_date):
    number_of_days = calculate_duration(start_date, end_date)
    return number_of_days * 100


# this method vectorizes user requests with the same vectorizer that was used to store all text files
def vectorize_user_request(user_request):
    embedding = client.embeddings.create(
        input=[user_request], model="text-embedding-3-large"
    ).data[0].embedding
    return struct.pack(f"{len(embedding)}f", *embedding)


# this method runs a vector search against the sqlite-vec virtual table
# and returns the contents of the closest source files
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
        with open(PROJECT_ROOT / file_path, "r") as f:
            texts.append(f.read())
    return texts


def give_tourist_information_space(user_request):
    packed = vectorize_user_request(user_request)
    return retrieve_closest_texts(packed)
