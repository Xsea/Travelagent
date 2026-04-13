import json

from openai import AzureOpenAI

from tools import calculate_hotel_cost, give_tourist_information_space
from tools_description import calculate_hotel_cost_tool, give_tourist_information_space_description

client = AzureOpenAI()

assistantMessage = "How can I help you?"
messages = [{"role": "system",
             "content": """You are a space traveling agent, responsible for helping people planning their vacations. 
             You live in a fictitious time, where travel to space is feasible for everyone, and flights only take one day
             Clients will come to you searching for advice on traveling locations. Please answer, so that they find a nice 
             location to spend their holidays. 
             If the user asks for location of space travel, you can use the answer_space_travel_questions tool. 
             Please answer questions for space travel seriously!
             """}]

tools = [calculate_hotel_cost_tool, give_tourist_information_space_description]
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
        elif tool_call.function.name == "answer_space_travel_questions":
            # get closest texts
            texts = give_tourist_information_space(arguments["user_request"])
            # if you want, make copy of messages to save some money (texts will not always be in the context)
            # however, maybe the chat flow will be better if it stays, you decide
            space_message = messages.copy()
            # add all texts to the chat history (or the copy of it)
            for text in texts:
                space_message.append(
                    {"role": "system",
                     "content": text})
            # generate new completion request
            completionRequest = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=space_message
                )

    llm_answer = completionRequest.choices[0].message
    messages.append(llm_answer)
    assistantMessage = llm_answer.content