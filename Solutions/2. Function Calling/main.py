import json

from openai import OpenAI

from tools import calculate_hotel_cost
from tools_description import calculate_hotel_cost_tool

client = OpenAI()

assistantMessage = "How can I help you?"
messages = [{"role": "system",
             "content": """You are a traveling agent, responsible for helping people planning their vacations.
             Users will come to you searching for advice on traveling locations. Please answer, so that they find a nice 
             location to spend their holidays
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

    llm_answer = completionRequest.choices[0].message
    messages.append(llm_answer)
    assistantMessage = llm_answer.content