import json

from exceptiongroup import catch
from openai import OpenAI

from tools import calculate_hotel_cost, give_tourist_information_space, list_hotels, give_hotel_information, \
    collect_information_from_the_user, book_hotel, book_flights
from tools_description import calculate_hotel_cost_tool_description, list_hotels_description, give_hotel_information_description, \
    give_tourist_information_space_description, book_hotel_description, book_flights_description, collect_information_from_the_user_description

client = OpenAI()

### Tools
tools = [calculate_hotel_cost_tool_description, give_tourist_information_space_description, list_hotels_description,
         give_hotel_information_description, book_hotel_description,
         book_flights_description, collect_information_from_the_user_description]

#### Planning
def planning(user_request, chat_history):
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
                 Give your answer in the following format (while filling out the {} with your own input:

                 STEP X:
                 Explanation: {What needs to be done}
                 Recommended Tool: {Your Tool Recommendation}
                 Suggested Input: {Using the input parameters of the tool, determine the suggested input. If the input is
                  dependent on the output of a previous step, write Output of Step Y}
                  
                Include all steps necessary to finish the task in your plan. Before writing down the plan however, 
                start by explaining your thoughts. A few notes for your planning: 
                1. When asked to book a hotel, you do not need to calculate the cost, as the booking function will do it
                2. Assume that the flight outbound and return dates are the same as the check in and check out dates for the hotel
                 """},

            {"role": "user", "content": user_request },
            {"role": "system", "content": chat_history }
            ]
        )
    return completion_plan.choices[0].message.content

### Memory
def memory(tool_name, arguments, output, step):
    # explain what happened in this step, so that the llm knows can decide the next step
    executed_step = "\n ****** EXECUTED STEP " + str(step+1) + " ******"
    if tool_name == "calculate_hotel_cost":
        executed_step += "\n We used tool calculate_hotel_cost to determine the costs with following arguments:"
        executed_step += f"\n ARGUMENTS: start_date: {arguments['start_date']} and end_date: {arguments['end_date']}"
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    elif tool_name == "test_writer":
        executed_step += "\n We used tool give_tourist_information_space to find tourist information:"
        executed_step += "\n ARGUMENTS: " + arguments["user_request"]
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    return executed_step


assistantMessage = "How can I help you?"
messages = [{"role": "system",
             "content": """You are a space traveling agent, responsible for helping people planning their vacations. 
             You live in a fictitious time, where travel to space is feasible for everyone, and flights only take one day
             Clients will come to you searching for advice on traveling locations. Please answer, so that they find a nice 
             location to spend their holidays. 
             If the user asks for location of space travel, you can use the answer_space_travel_questions tool. 
             Please answer questions for space travel seriously!
             
             """}]

def flatten_history(messages_array):
    history = ""
    for message in messages_array:
        history = message["role"] + ": " + message["content"] + "\n"
    return history

while True:
    userRequest = str(input(assistantMessage + "\n"))
    if userRequest == "thanks":
        break
    messages.append({"role": "user", "content": userRequest})
    # read user input and devise a plan on how to solve it
    the_plan = planning(userRequest, flatten_history(messages))
    print(the_plan)
    i = 0
    executed_steps = "########## EXECUTED STEPS ############"
    while i < 20:
        print("########### STEP {0} ######################".format(i + 1))
        # we start by analyzing the plan and the executed steps -> this will determine the next step
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
                    Remember, that you have not parallel tool use capability.
                    Please output your suggestion for a next step in the following valid JSON format with the following way 
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
                    "content": the_plan
                    },
                {
                    "role": "system",
                    "content": executed_steps
                    }
                ]
            )
        next_step = completion_step.choices[0].message.content
        print("########## WE WILL DO THE FOLLOWING: \n", next_step + "\n############\n")

        # sometimes the LLM creates a valid json, but starts with the annotation ```json then {} and ends with ```
        next_step = next_step.removeprefix("```json").removesuffix("```")
        next_step_parsed = json.loads(next_step)

        # we are done - lets get out
        if next_step_parsed["finish"]:
            break

        # now we use the determined next plan and execuWrite two methods, one that calculates the fibonacci sequence iteratively and one that implements the rock paper scissors gamete the tool - needs separation as text generation and tool call can
        # not be done simultaneously
        completion_tool = client.chat.completions.create(
            model="gpt-4o-mini",
            tools=tools,
            tool_choice='required',
            messages=[
                {"role": "system",
                 "content": """Read the assistant message below and determine which tool to use to satisfy this task"""},
                {
                    "role": "assistant",
                    "content": str(next_step_parsed["nextStep"])
                    }
                ]
            )

        # save what we have done - this is our short term memory.
        # The LLM will use this to determine what has been done and what needs to be done next

    completionRequest = client.chat.completions.create(
        model="gpt-4o",
        tools=tools,
        messages=messages
        )

    if completionRequest.choices[0].finish_reason == "tool_calls":
        tool_call = completionRequest.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        output = ""
        try:
            if tool_call.function.name == "calculate_hotel_cost":
                output = calculate_hotel_cost(arguments["start_date"], arguments["end_date"])
            elif tool_call.function.name == "give_tourist_information_space":
                output = give_tourist_information_space(arguments["user_request"])
            elif tool_call.function.name == "list_hotels":
                output = list_hotels(arguments["location"])
            elif tool_call.function.name == "give_hotel_information":
                output = give_hotel_information(arguments["hotel_name"])
            elif tool_call.function.name == "collect_information_from_the_user_description":
                output = collect_information_from_the_user(arguments["question"])
            elif tool_call.function.name == "book_hotel":
                output = book_hotel(arguments["hotel_name"], arguments["check_in"], arguments["check_out"])
            elif tool_call.function.name == "book_flights":
                output = book_flights(arguments["arrival_port"], arguments["outbound_date"], arguments["return_date"])
            this_step = memory(tool_call.function.name, arguments, output, i)
            print(this_step)
            executed_steps += this_step
        except Exception as error:
            this_step = f"error while calling {tool_call.function.name} with arguments {arguments}. Error Message: {error}"




    llm_answer = completionRequest.choices[0].message
    messages.append(llm_answer)
    assistantMessage = llm_answer.content