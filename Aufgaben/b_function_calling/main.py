import json

from openai import AzureOpenAI

from tools import calculate_hotel_cost
from tools_description import calculate_hotel_cost_tool

client = AzureOpenAI()

assistantMessage = "How can I help you?"
messages = [{"role": "system",
             "content": """You are a traveling agent, responsible for helping people planning their vacations.
             Users will come to you searching for advice on traveling locations. Please answer, so that they find a nice 
             location to spend their holidays
             """}]

# add a tool to this array
tools = []
while True:
    userRequest = str(input(assistantMessage + "\n"))
    if userRequest == "thanks":
        break

    messages.append({"role": "user", "content": userRequest})
    # fill the tools property in the completion request
    completionRequest = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= messages
    )

    # check the finish reason of completionRequest.choices[0] -> if tool_calls start separate handling
    # in completionRequest.choices[0].message.tool_calls[0] you will find the name of the called tool
    # this line "arguments = json.loads(tool_call.function.arguments)" extracts the json properties into an array.
    # for example, you can then use "start = arguments["start_date"]" to extract the needed information
    # after you have calculated the cost: How do you now get this information to the LLM?
    # And how do you get the answer the LLM would generate?

    ##########################
    llm_answer = completionRequest.choices[0].message
    messages.append(llm_answer)
    assistantMessage = llm_answer.content