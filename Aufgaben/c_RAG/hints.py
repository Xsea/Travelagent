try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3
import struct
from pathlib import Path

import sqlite_vec
from openai import AzureOpenAI

DB_PATH = Path(__file__).resolve().parent.parent.parent / "travel.db"

con = sqlite3.connect(DB_PATH)
con.enable_load_extension(True)
sqlite_vec.load(con)
con.enable_load_extension(False)

client = AzureOpenAI()

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
