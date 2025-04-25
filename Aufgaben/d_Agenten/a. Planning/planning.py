from Aufgaben.d_Agenten.tools_description import tool_belt
#### Planning
def planning(user_request: str, chat_history: str, tools):
    ### Design a prompt that generates a plan for the agent
    ### it is helpful to tell the LLM in which format the output should be
    ### do not worry about the chat history too much, just add it as another system message. We will provide the correct
    ### method for it

    completion_plan = client.chat.completions.create(
        model="gpt-4o",
        tools=tools,
        tool_choice='none',
        messages=[
            {"role": "system",
             "content": """ ############# """},

            {"role": "user", "content": user_request},
            {"role": "system", "content": chat_history}
            ]
        )
    return completion_plan.choices[0].message.content

print(planning("Please book a hotel on mars for me", "", tool_belt))
