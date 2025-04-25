import json

from openai import OpenAI

from tools import calculate_hotel_cost
from tools_description import calculate_hotel_cost_tool

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

tools = [calculate_hotel_cost_tool]
while True:
    userRequest = str(input(assistantMessage + "\n"))
    if userRequest == "thanks":
        break
    messages.append({"role": "user", "content": userRequest})
    # read user input and devise a plan on how to solve it
    completionRequest = client.chat.completions.create(
        model="gpt-4o-mini",
        tools=tools,
        messages= messages
        )

    if completionRequest.choices[0].finish_reason == "tool_calls":
        tool_call = completionRequest.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        if tool_call.function.name == "calculate_hotel_cost":
            cost = calculate_hotel_cost(arguments["start_date"], arguments["end_date"])
            messages.append({"role": "system",
             "content": """The cost of the stay with arrival date {} and departure date {} will be {}""".format(
                 arguments["start_date"], arguments["end_date"], cost
                 )})
            completionRequest = client.chat.completions.create(
                model="gpt-4o-mini",
                messages= messages
            )
        # add a new tool to the descriptions, that describes a tool that is able to get information about space locations
        # add this tool here with an if condition and call a method that does the following:
        # 1. vectorizes the user_request (submethod is available in hints folder)
        # 2. gets the closest texts for the user request (submethod is available in hints folder)
        # 3. adds the texts to the chat history. Here you can decide, if you want to make a
        # temporary copy and fill it with the texts. This will save you costs,
        # as not always the full texts are part of the context, but may make the results worse (try out if you want)
        # create a new completion request and give the result to the user (and also save it in messages)


    llm_answer = completionRequest.choices[0].message
    messages.append(llm_answer)
    assistantMessage = llm_answer.content