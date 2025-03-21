import os
import psycopg2
import tiktoken
from openai import OpenAI

# To get the tokeniser corresponding to a specific model in the OpenAI API:
tokenizer = tiktoken.encoding_for_model("gpt-4o")
client = OpenAI()
db_params = {
    'dbname': 'vectorDB',
    'user': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': 5432
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

# Tokenize the text into words
def chunker(text):
    words = text.replace("\n", " ").split()

    # Initialize variables
    chunk_length = 128  # Specify the chunk length
    current_chunk = []
    current_chunk_length = 0
    chunks = []

    # Process each word
    for word in words:
        word_tokens = tokenizer.encode(word + " ")  # Encode the word with a space
        word_length = len(word_tokens)

        # Check if adding the word exceeds the chunk length
        if current_chunk_length + word_length > chunk_length:
            # If it does, finalize the current chunk and start a new one
            chunks.append(current_chunk)
            current_chunk = word_tokens
            current_chunk_length = word_length
        else:
            # Otherwise, add the word to the current chunk
            current_chunk.extend(word_tokens)
            current_chunk_length += word_length

    # Add the last chunk if it has content
    if current_chunk:
        chunks.append(current_chunk)

    # Decode the token chunks back into text
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]

    # Generate Vectors

    return text_chunks

def vectorize_chunks(chunks):
    vectors = []
    for chunk in chunks:
        vector = client.embeddings.create(input=[chunk], model="text-embedding-3-large").data[0].embedding
        vectors.append(vector)
    return vectors

def fill_into_table(file_name, vectors):
    for index in range(len(vectors)):
        insert_query = '''
            INSERT INTO space_travel_vectors (name, chunk_id, vector_column)
            VALUES (%s, %s, %s);
            '''
        cursor.execute(insert_query, (file_name, index, vectors[index]))
        connection.commit()

topFolder = "../Space Destinations"
folders = os.listdir(topFolder)
for folder in folders:
    folderPath = topFolder + "/"+ folder
    files = os.listdir(folderPath)
    for file_name in files:
        if "prompt" in file_name:
            continue
        filePath = folderPath + "/" + file_name
        print(filePath)
        # Your large body of text
        with open(filePath, 'r') as file:
            text = file.read()
        chunks = chunker(text)
        vectors = vectorize_chunks(chunks)
        fill_into_table(filePath.replace("..", "."), vectors)