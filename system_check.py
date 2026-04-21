"""Smoke test: verifies sqlite-vec + Azure OpenAI are wired up correctly.

Run from the project root:
    python system_check.py
Then answer "Tell me about Mars!" — you should see a Mars travel response.
"""
try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3
import struct
from pathlib import Path

import sqlite_vec
from openai import AzureOpenAI

DB_PATH = Path(__file__).resolve().parent / "travel.db"

con = sqlite3.connect(DB_PATH)
con.enable_load_extension(True)
sqlite_vec.load(con)
con.enable_load_extension(False)

client = AzureOpenAI()


def vectorize_user_request(user_request):
    embedding = client.embeddings.create(
        input=[user_request], model="text-embedding-3-large"
    ).data[0].embedding
    return struct.pack(f"{len(embedding)}f", *embedding)


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
        with open(Path(__file__).resolve().parent / file_path, "r") as f:
            texts.append(f.read())
    return texts


def answer_space_travel(message: str):
    packed = vectorize_user_request(message)
    texts = retrieve_closest_texts(packed)
    return texts[0]


messages = [
    {
        "role": "system",
        "content": (
            "You are a space traveling agent, responsible for helping people planning their vacations. "
            "You live in a fictitious time, where travel to space is feasible for everyone, and flights only take one day. "
            "Clients will come to you searching for advice on traveling locations. Please answer, so that they find a nice "
            "location to spend their holidays."
        ),
    }
]

user_request = input("Type: 'Tell me about Mars!'")
text = answer_space_travel(user_request)
messages.append({"role": "user", "content": user_request})
messages.append({"role": "system", "content": text})

completion = client.chat.completions.create(model="gpt-5.4-mini", messages=messages)
print(completion.choices[0].message.content)
