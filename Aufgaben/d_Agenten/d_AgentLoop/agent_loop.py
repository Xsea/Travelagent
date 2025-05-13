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
    ############
    ## First, user your method to make a plan
    ############
    i = 0
    executed_steps = "########## EXECUTED STEPS ############"
    while i < 20:
        ############
        ## now we figure out the next step
        ############

        ############
        ## sometimes the LLM creates a valid json, but starts with the annotation ```json then {} and ends with ```
        ## so here is the code to remove this annoying part:
        #next_step_result = next_step_result.removeprefix("```json").removesuffix("```")
        #next_step_parsed = json.loads(next_step_result)
        ############

        ############
        ## break the loop here, if the next_steps says, that it is done
        ############

        ############
        ## now we need to determine the tool
        ############

        ############
        ## and then execute this tool
        ## while we execute tool, we use the output to update our executed_steps by calling the short_term_memory
        ############
        i += 1
    return executed_steps

print(agent_loop("Please book a hotel on mars for me", ""))

