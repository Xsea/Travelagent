import json

from exceptiongroup import catch
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

#### Planning
def planning(user_request, chat_history):
    ### Design a prompt that generates a plan for the agent

### Memory
def memory():
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
    # read user input and devise a plan on how to solve it
    the_plan = planning()
    print(the_plan)
    i = 0
    # Now comes the agent loop!
    # Following needs to happen: We need to read out the plan and compare it against all executed steps
    # this will help us to identify the next step
    # using the output of the next step, determine which tool to use
    # after the tool has been determined, we need to call our method
    # then use the memory to update our executed steps



    # in the end, use the executed steps to write a summary for the user to print


    llm_answer =
    messages.append({"role": "assistant", "content": llm_answer})
    assistantMessage = llm_answer