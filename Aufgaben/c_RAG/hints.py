"""Hints for the RAG exercise: ready-made vectorize + retrieve helpers."""
import sqlite3
import struct
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


# this method vectorizes user requests with the same vectorizer that was used to store all text files
def vectorize_user_request(user_request):
    embedding = client.embeddings.create(
        input=[user_request], model="text-embedding-3-large"
    ).data[0].embedding
    return struct.pack(f"{len(embedding)}f", *embedding)


# this method does a vector search against the sqlite-vec virtual table.
# It returns the texts of the 5 chunks closest to the query vector (deduplicated by file).
# Play around with the LIMIT, the source columns, or the prompt for very different results.
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
