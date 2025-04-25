##### PLANNING HINT 1 #########

def planning(user_request, chat_history):
    completion_plan = client.chat.completions.create(
        model="gpt-4o",
        tools=tools,
        tool_choice='none',
        messages=[
            {"role": "system",
             "content": """
                ### ADD GENERAL DESCRIPTION OF TASK HERE

                 ######### ADD OUTPUT FORMAT HERE
                 """},

            {"role": "user", "content": user_request},
            {"role": "system", "content": chat_history}
            ]
        )
    return completion_plan.choices[0].message.content

### SHORT TERM MEMORY HINT 1

def short_term_memory(tool_name, arguments, output, step):
    # explain what happened in this step, so that the llm knows can decide the next step
    executed_step = "\n ****** EXECUTED STEP " + str(step+1) + " ******"
    if tool_name == "calculate_hotel_cost":
    elif tool_name == "give_tourist_information_space":
    elif tool_name == "list_hotels":
    elif tool_name == "give_hotel_information":
    elif tool_name == "collect_information_from_the_user":
    elif tool_name == "book_hotel":
    elif tool_name == "book_flights":
    return executed_step


#### AGENT LOOP HINT 1
 while i < 20:
        print("########### STEP {0} ######################".format(i + 1))
        # we start by analyzing the plan and the executed steps -> this will determine the next step
        completion_step = client.chat.completions.create(
            model="gpt-4o",
            tools=tools,
            tool_choice='none',
            messages=[
                {"role": "system",
                 "content": """
                    """},
                {
                    "role": "system",
                    "content": the_plan
                    },
                {
                    "role": "system",
                    "content": executed_steps
                    },
                {
                    "role": "system",
                    "content": flatten_history(messages)
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
                 "content": """ ADD PROMPT HERE """},
                {
                    "role": "assistant",
                    "content": str(next_step_parsed["nextStep"])
                    }
                ]
            )
        ### NOW USE THE TOOL OUTPUT TO CALL THE CORRECT FUNCTION
        i += 1


### AGENT LOOP HINT 2
        ### FUNCTION CALLIN
        if completion_tool.choices[0].finish_reason == "tool_calls":
            tool_call = completion_tool.choices[0].message.tool_calls[0]
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
                elif tool_call.function.name == "collect_information_from_the_user":
                    output = collect_information_from_the_user(arguments["question"])
                elif tool_call.function.name == "book_hotel":
                    output = book_hotel(arguments["hotel_name"], arguments["check_in"], arguments["check_out"])
                elif tool_call.function.name == "book_flights":
                    output = book_flights(arguments["arrival_port"], arguments["outbound_date"], arguments["return_date"])
                this_step = short_term_memory(tool_call.function.name, arguments, output, i)
                print(this_step)
                executed_steps += this_step
            except Exception as error:
                this_step = f"error while calling {tool_call.function.name} with arguments {arguments}. Error Message: {error}"
            i += 1