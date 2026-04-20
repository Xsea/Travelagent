from openai import AzureOpenAI
from Aufgaben.d_Agenten.tools_description import tool_belt
from Aufgaben.d_Agenten.a_Planning.examplePlan import  plan as the_plan

client = AzureOpenAI()

def next_step(plan, executed_steps, chat_history, tools):
    completion_step = client.chat.completions.create(
            model="gpt-5.4-mini",
            tools=tools,
            tool_choice='none',
            messages=[
                {"role": "system",
                 "content": """ Your task is to determine which tool will be used next. You are a reasoning step in between
                    This is why you are given tools, but are not allowed to use them. You should reason, with the explanation
                    following which tool to use next. So it is your task, to do this, so the rest can follow after.
                    So do not reason about not being allowed to use tools. This is on purpose. You should help to set up
                    the next step. You can not use tools and this is fine and on purpose. Do not think about that, but 
                    rather what the next step should be, which tool can help the user!
                    The next message you will receive is a step by step plan of a task we need to execute.
                    Its format contains the order of the steps, an explanation of what needs to be done, a recommended tool,
                    as well as the suggested input. The input can be given directly, or as the output of a previously executed step.
                    The second message will contain a list of steps that we have already executed with its format containing
                    the order of the steps, the tool that was used, the argument that was given and if applicable the generated output.
                    This output might be needed to execute further steps later on
                    If this list is empty, no steps have been executed until now.
                    Compare the plan and the executed list with each other to determine the next step that needs to be executed. 
                    Try to hold as close to the plan as possible and only deviate, if the user responses require it, or
                    the tools outputs reveal errors
                    Please output your suggestion for a next step in the following valid JSON format with the following way 
                    No multi tool use parallel! Always only give one tool recommendation
                    You also get access to the chat history below.
                    If you need to ask the user for questions, then use the ask collect_information_from_the_user tool,
                    so note this in next_step.
                    Remember! You are a space travel agent! Space travel is possible in your world and if you need any
                    information to help with space travel questions, use your tools!
                    ONLY ANSWER WITH JSON, USE THE FORMAT BELOW. DO NOT FORMAT THE MESSAGE, JUST ANSWER WITH JSON.
                    (Read the Text between $$ as explanations of the parameter):
                    {
                       "chainOfThoughts": $Your thoughts which tool the next LLM should use. You will not use it and this is fine$
                       "nextStep": $leave this object null if no step is needed$ {
                           "recommendedTool": $Your tool recommendation. To determine this look at your available tools$
                           "Input": $The input needed. Either determined by you, or use the output of a previous step$
                       }
                       "finish": $Boolean parameter, fill with false if you determine there is a next step, true if you determine the task is solved
                    }
                    """},
                {
                    "role": "system",
                    "content": plan
                    },
                {
                    "role": "system",
                    "content": executed_steps
                    },
                {
                    "role": "system",
                    "content": chat_history
                    }
                ]
            )
    print(completion_step)
    return completion_step.choices[0].message.content

if __name__ == "__main__":
    print(next_step(the_plan, "", "", tool_belt))