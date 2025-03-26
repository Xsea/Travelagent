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

assistantMessage = "How can I help you?"
messages = [{"role": "system",
             "content": """You are a space traveling agent, responsible for helping people planning their vacations. 
             You live in a fictitious time, where travel to space is feasible for everyone, and flights only take one day
             Clients will come to you searching for advice on traveling locations. Please answer, so that they find a nice 
             location to spend their holidays. 
             If the user asks for location of space travel, you can use the answer_space_travel_questions tool. 
             Please answer questions for space travel seriously!
             """}]

userRequest = str(input(assistantMessage + "\n"))

messages.append({"role": "user", "content": userRequest})
completionRequest = client.chat.completions.create(
    model="gpt-4o-mini",
    messages= messages
    )

llm_answer = completionRequest.choices[0].message
print(llm_answer)