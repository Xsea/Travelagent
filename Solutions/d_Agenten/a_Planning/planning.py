from Aufgaben.d_Agenten.tools_description import tool_belt
from openai import OpenAI

client = OpenAI()

#### Planning
def planning(user_request: str, chat_history: str, tools):
    completion_plan = client.chat.completions.create(
        model="gpt-4o",
        tools=tools,
        tool_choice='none',
        messages=[
            {"role": "system",
             "content": """You are a space travel agent who has to determine how to solve a task given by the user. 
                 You do not solve tasks yourself, but only determine the step by step plan given your accessible tools.
                 You also have access to the chat history that was provided until now, check there if the necessary 
                 information is already available and which you still need to collect.
                Include all steps necessary to finish the task in your plan. Before writing down the plan however, 
                start by explaining your thoughts. A few notes for your planning: 
                1. When asked to book a hotel, you do not need to calculate the cost, as the booking function will do it
                2. Assume that the flight outbound and return dates are the same as the check in and check out dates for the hotel
                3. Search through the chat history to determine location, hotels or dates that have already been mentioned by the user
                4. Always give the full plan! You might first need just one information, but you can anticapte more steps. 
                This means, give all the steps needed to gather all the information and do all necessary action!

                 Give your answer in the following format (while filling out the {} with your own input:

                 STEP X:
                 Explanation: {What needs to be done}
                 Recommended Tool: {Your Tool Recommendation}
                 Suggested Input: {Using the input parameters of the tool, determine the suggested input. If the input is
                  dependent on the output of a previous step, write Output of Step Y}
                 """},

            {"role": "user", "content": user_request},
            {"role": "system", "content": chat_history}
            ]
        )
    return completion_plan.choices[0].message.content

if __name__ == "__main__":
    print(planning("Please book a hotel on mars for me", "", tool_belt))
