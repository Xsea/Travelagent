from openai import AzureOpenAI
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

client = AzureOpenAI()


def vectorize_user_request(user_request):
    return client.embeddings.create(input=[user_request], model="text-embedding-3-large").data[0].embedding

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

def answer_space_travel(user_request):
    # vectorize user request
    vector = vectorize_user_request(user_request)
    # retrieve the closest texts
    texts = retrieve_closest_texts(vector)
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
    model="gpt-4o-mini",
    messages= messages
    )

llm_answer = completionRequest.choices[0].message.content
print(llm_answer)

