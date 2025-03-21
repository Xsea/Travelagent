from openai import OpenAI
import psycopg2

db_params = {
    'dbname': 'vectorDB',
    'user': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': 5432
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()


client = OpenAI()

# this method vectorizes user requests with the same vectorizer that was used to store all text files
def vectorize_user_request(user_request):
    return client.embeddings.create(input=[user_request], model="text-embedding-3-large").data[0].embedding

# this method uses an SQL request on the pgvector database
# using the cosine distance, we find the 5 closest matching chunks, and return the corresponding texts
# you can play around here for very different results
def retrieve_closest_texts(vector):
    texts = []
    select_query = f"SELECT * FROM space_travel_vectors ORDER BY vector_column <=> '{vector}' LIMIT 5;"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    # return the texts of the files
    named_files = []
    for row in rows:
        named_files.append(row[1])
    for file in set(named_files):
        with open(file, 'r') as f:
            texts.append(f.read())
    return texts