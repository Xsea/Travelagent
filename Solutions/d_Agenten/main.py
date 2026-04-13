import json

from openai import AzureOpenAI

from Solutions.d_Agenten.d_AgentLoop.agent_loop import agent_loop
from tools import calculate_hotel_cost, give_tourist_information_space, list_hotels, give_hotel_information, \
    collect_information_from_the_user, book_hotel, book_flights
from tools_description import calculate_hotel_cost_tool_description, list_hotels_description, \
    give_hotel_information_description, \
    give_tourist_information_space_description, book_hotel_description, book_flights_description, \
    collect_information_from_the_user_description

client = AzureOpenAI()
assistantMessage = "How can I help you?"
messages = [{"role": "system",
             "content": """You are a space traveling agent, responsible for helping people planning their vacations. 
             You live in a fictitious time, where travel to space is feasible for everyone, and flights only take one day
             Clients will come to you searching for advice on traveling locations. Please answer, so that they find a nice 
             location to spend their holidays. 
             If the user asks for location of space travel, you can use the give_tourist_information_space tool. 
             Please answer questions for space travel seriously!

             """}]

def flatten_history(messages_array):
    history = ""
    for message in messages_array:
        history = message["role"] + ": " + message["content"] + "\n"
    return history

while True:
    user_request = str(input(assistantMessage + "\n"))
    if user_request == "thanks":
        break
    messages.append({"role": "user", "content": user_request})
    # read user input and devise a plan on how to solve it
    executed_steps = agent_loop(user_request, flatten_history(messages))

    summaryRequest = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system",
                   "content": """As a travel agent, you have received a user_request (see below). Additionally, you tried
                  to fulfill the request step by step (see the executed steps in the system message). Please write an answer
                  to the user_request, given the executed steps."""},
                  {"role": "user", "content": user_request},
                  {"role": "system",
                   "content": executed_steps}
                  ]
        )

    llm_answer = summaryRequest.choices[0].message.content
    messages.append({"role": "assistant", "content": llm_answer})
    assistantMessage = llm_answer
