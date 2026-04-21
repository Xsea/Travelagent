from openai import AzureOpenAI
from Aufgaben.d_Agenten.tools_description import tool_belt
from Aufgaben.d_Agenten.a_Planning.examplePlan import  plan as the_plan

client = AzureOpenAI()


def tools_to_text(tools):
    lines = []
    for t in tools:
        f = t["function"]
        lines.append(f"Tool: {f['name']}")
        lines.append(f"  Description: {f['description']}")
        lines.append(f"  Parameters:")
        for param, info in f["parameters"]["properties"].items():
            required = param in f["parameters"].get("required", [])
            req_label = " (required)" if required else " (optional)"
            lines.append(f"    - {param} ({info['type']}{req_label}): {info['description']}")
        lines.append("")
    return "\n".join(lines)

def next_step(plan, executed_steps, chat_history, tools):
    tool_text = tools_to_text(tools)
    completion_step = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {"role": "system",
                 "content": f"""You are a tool router. Your ONLY job is to output JSON recommending which tool the next LLM should call.
                  You do NOT execute tools — you RECOMMEND them for the next LLM.
                
                  Available tools:
                  {tool_text}
                
                  The next message contains a step-by-step plan. The second message contains already executed steps.
                  Compare them to determine the next step.
                  Hold close to the plan and only deviate if user responses or tool outputs reveal errors.
                  No multi tool use parallel — always only give one tool recommendation.
                  If you need to ask the user a question, recommend the collect_information_from_the_user tool.
                  If a hotel is unavailable, gather the availability options to help the user.
                  You are a space travel agent — space travel is possible in your world!
                
                  ONLY ANSWER WITH JSON, no formatting, no markdown:
                  {{
                     "chainOfThoughts": "<your reasoning about which tool the next LLM should use>",
                     "nextStep": {{
                         "recommendedTool": "<tool name from the available tools list>",
                         "Input": "<the input needed, either determined by you or from a previous step's output>"
                     }},
                     "finish": <false if there is a next step, true if the task is solved>
                  }}
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