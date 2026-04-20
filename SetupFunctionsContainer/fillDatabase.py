import os
import struct

try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

import sqlite_vec
import tiktoken
from openai import AzureOpenAI

tokenizer = tiktoken.encoding_for_model("gpt-5.4-mini")
client = AzureOpenAI()

con = sqlite3.connect("../travel.db")
con.enable_load_extension(True)
sqlite_vec.load(con)
con.enable_load_extension(False)


def pack_vector(values):
    return struct.pack(f"{len(values)}f", *values)


def chunker(text):
    words = text.replace("\n", " ").split()

    chunk_length = 128
    current_chunk = []
    current_chunk_length = 0
    chunks = []

    for word in words:
        word_tokens = tokenizer.encode(word + " ")
        word_length = len(word_tokens)

        if current_chunk_length + word_length > chunk_length:
            chunks.append(current_chunk)
            current_chunk = word_tokens
            current_chunk_length = word_length
        else:
            current_chunk.extend(word_tokens)
            current_chunk_length += word_length

    if current_chunk:
        chunks.append(current_chunk)

    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]
    return text_chunks


def vectorize_chunks(chunks):
    vectors = []
    for chunk in chunks:
        vector = client.embeddings.create(input=[chunk], model="text-embedding-3-large").data[0].embedding
        vectors.append(vector)
    return vectors


def fill_into_table(file_name, vectors):
    for index in range(len(vectors)):
        con.execute(
            "INSERT INTO space_travel_vectors (name, chunk_id, embedding) VALUES (?, ?, ?)",
            (file_name, index, pack_vector(vectors[index])),
        )
    con.commit()


topFolder = "../Space Destinations"
folders = os.listdir(topFolder)
for folder in folders:
    folderPath = topFolder + "/" + folder
    files = os.listdir(folderPath)
    for file_name in files:
        if "prompt" in file_name:
            continue
        filePath = folderPath + "/" + file_name
        print(filePath)
        with open(filePath, 'r') as file:
            text = file.read()
        chunks = chunker(text)
        vectors = vectorize_chunks(chunks)
        fill_into_table(filePath.replace("..", "."), vectors)
