from openai import AzureOpenAI
from Aufgaben.d_Agenten.tools_description import tool_belt
from Aufgaben.d_Agenten.a_Planning.examplePlan import  plan as the_plan

client = AzureOpenAI()

def next_step(plan, executed_steps, chat_history, tools):
    completion_step = client.chat.completions.create(
            model="gpt-4o",
            tools=tools,
            tool_choice='none',
            messages=[
                {"role": "system",
                 "content": """The next message you will receive is a step by step plan of a task we need to execute.
                    Its format contains the order of the steps, an explanation of what needs to be done, a recommended tool,
                    as well as the suggested input. The input can be given directly, or as the output of a previously executed step.
                    The second message will contain a list of steps that we have already executed with its format containing
                    the order of the steps, the tool that was used, the argument that was given and if applicable the generated output.
                    This output might be needed to execute further steps later on
                    If this list is empty, no steps have been executed until now.
                    Compare the plan and the executed list with each other to determine the next step that needs to be executed. 
                    Do only execute steps, that have been mentioned in the plan! Do not add more steps than suggested.
                    Please output your suggestion for a next step in the following valid JSON format with the following way 
                    No multi tool use parallel! Always only give one tool recommendation
                    You also get access to the chat history below.
                    ONLY ANSWER WITH JSON, USE THE FORMAT BELOW. DO NOT FORMAT THE MESSAGE, JUST ANSWER WITH JSON.
                    (Read the Text between $$ as explanations of the parameter):
                    {
                       "chainOfThoughts": $Your chain of thoughts while solving this tasks. Fill it with your reasoning$
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
    return completion_step.choices[0].message.content

if __name__ == "__main__":
    print(next_step(the_plan, "", "", tool_belt))