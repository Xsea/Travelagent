import json

from openai import OpenAI

from Aufgaben.d_Agenten.tools_description import tool_belt
from Solutions.d_Agenten.a_Planning.planning import planning
from Solutions.d_Agenten.b_Agent.next_step import next_step
from Solutions.d_Agenten.b_Agent.tool_determination import determine_tool
from Solutions.d_Agenten.b_Agent.tool_execution import tool_execution
from Solutions.d_Agenten.c_Memory.short_term_memory import short_term_memory

client = OpenAI()
def agent_loop(user_request, chat_history):
    the_plan = planning(user_request, chat_history, tool_belt)
    i = 0
    executed_steps = "########## EXECUTED STEPS ############"
    while i < 20:
        print("########### STEP {0} ######################".format(i + 1))
        # we start by analyzing the plan and the executed steps -> this will determine the next step

        next_step_result = next_step(the_plan, executed_steps, chat_history, tool_belt)
        print("########## WE WILL DO THE FOLLOWING: \n", next_step_result + "\n############\n")

        # sometimes the LLM creates a valid json, but starts with the annotation ```json then {} and ends with ```
        next_step_result = next_step_result.removeprefix("```json").removesuffix("```")
        next_step_parsed = json.loads(next_step_result)

        # we are done - lets get out
        if next_step_parsed["finish"]:
            break

        # now we determine the next tool and then execute it
        tool = determine_tool(str(next_step_parsed["nextStep"]), tool_belt)

        if tool.finish_reason == "tool_calls":
            tool_call = tool.message.tool_calls[0]
            output = tool_execution(tool_call)
            executed_steps = short_term_memory(tool_call, output, i)
        i += 1
    return executed_steps

if __name__ == "__main__":
    print(agent_loop("Please book a hotel on mars for me", ""))