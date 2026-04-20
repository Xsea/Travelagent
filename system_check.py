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


def answer_space_travel(user_request):
    packed = vectorize_user_request(user_request)
    texts = retrieve_closest_texts(packed)
    return texts[0]

assistantMessage = "Ask me about Mars!"
messages = [{"role": "system",
             "content": """You are a space traveling agent, responsible for helping people planning their vacations.
             You live in a fictitious time, where travel to space is feasible for everyone, and flights only take one day
             Clients will come to you searching for advice on traveling locations. Please answer, so that they find a nice
             location to spend their holidays.
             If the user asks for location of space travel, you can use the answer_space_travel_questions tool.
             Please answer questions for space travel seriously!
             """}]

userRequest = str(input(assistantMessage + "\n"))
text = answer_space_travel(userRequest)
messages.append({"role": "user", "content": userRequest})
messages.append({"role": "system", "content": text})
completionRequest = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=messages
    )

llm_answer = completionRequest.choices[0].message.content
print(llm_answer)
