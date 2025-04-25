import json

from openai import OpenAI

from tools import calculate_hotel_cost, give_tourist_information_space, list_hotels, give_hotel_information, \
    collect_information_from_the_user, book_hotel, book_flights
from tools_description import calculate_hotel_cost_tool_description, list_hotels_description, give_hotel_information_description, \
    give_tourist_information_space_description, book_hotel_description, book_flights_description, collect_information_from_the_user_description

client = OpenAI()

### Tools
tools = [calculate_hotel_cost_tool_description, give_tourist_information_space_description, list_hotels_description,
         give_hotel_information_description, book_hotel_description,
         book_flights_description, collect_information_from_the_user_description]



### Short term memory
def short_term_memory():
    # design a method that takes all necessary information and writes a small summary of the step
    # this helps the LLM to identify the tasks that have been done


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
    chat_history = flatten_history(messages)
    ## get the plan for the user request

    ## run the agent

    # use the output to let an llm write a summary of what was done and give it as output to the user

    llm_answer =
    messages.append({"role": "assistant", "content": llm_answer})
    assistantMessage = llm_answer