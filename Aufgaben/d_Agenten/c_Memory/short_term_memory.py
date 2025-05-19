def short_term_memory(tool_name, arguments, output, step):
    # explain what happened in this step, so that the llm knows can decide the next step
    ## relevant points are: The used tool, the arguments that were used with the tool and the output of the method
    executed_step = "\n ****** EXECUTED STEP " + str(step + 1) + " ******"
    if tool_name == "calculate_hotel_cost":
        executed_step += ""
    elif tool_name == "give_tourist_information_space":
        executed_step += ""
    elif tool_name == "list_hotels":
        executed_step += ""
    elif tool_name == "give_hotel_information":
        executed_step += ""
    elif tool_name == "collect_information_from_the_user":
        executed_step += ""
    elif tool_name == "book_hotel":
        executed_step += ""
    elif tool_name == "book_flights":
        executed_step += ""
    return executed_step


if __name__ == "__main__":
    print(short_term_memory("calculate_hotel_cost", {'start_date': '2024-03-27', 'end_date': '2024-04-10', 'price': 235}, "3290", 0))
