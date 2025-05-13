import json

from Solutions.d_Agenten.b_Agent.tool_determination import determine_tool
from Solutions.d_Agenten.tools_description import tool_belt


def short_term_memory(tool, output, step):
    # explain what happened in this step, so that the llm knows can decide the next step
    arguments = json.loads(tool.function.arguments)
    tool_name = tool.function.name
    executed_step = "\n ****** EXECUTED STEP " + str(step + 1) + " ******"
    if tool_name == "calculate_hotel_cost":
        executed_step += "\n We used tool calculate_hotel_cost to determine the costs with following arguments:"
        executed_step += f"\n ARGUMENTS: start_date: {arguments['start_date']} and end_date: {arguments['end_date']}"
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    elif tool_name == "give_tourist_information_space":
        executed_step += "\n We used tool give_tourist_information_space to find tourist information:"
        executed_step += "\n ARGUMENTS: " + arguments["user_request"]
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    elif tool_name == "list_hotels":
        executed_step += "\n We used tool list_hotels to get a list of all hotels:"
        executed_step += "\n ARGUMENTS: " + arguments["location"]
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    elif tool_name == "give_hotel_information":
        executed_step += "\n We used tool give_hotel_information to get information for a specific hotel:"
        executed_step += "\n ARGUMENTS: " + arguments["hotel_name"]
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    elif tool_name == "collect_information_from_the_user":
        executed_step += "\n We used tool collect_information_from_the_user to gain additional information from the user:"
        executed_step += "\n ARGUMENTS: " + arguments["question"]
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    elif tool_name == "book_hotel":
        executed_step += "\n We used tool book_hotel to book a hotel:"
        executed_step += f"\n ARGUMENTS: hotel_name: {arguments['hotel_name']}, check_in: {arguments['check_in']}, check_out: {arguments['check_out']}"
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    elif tool_name == "book_flights":
        executed_step += "\n We used tool book_flights to book flights:"
        executed_step += f"\n ARGUMENTS: arrival_port: {arguments['arrival_port']}, outbound_date: {arguments['outbound_date']}, return_date: {arguments['return_date']}"
        executed_step += "\n OUTPUT OF STEP" + str(step) + "\n" + output + "\n END OUTPUT"
    return executed_step

if __name__ == "__main__":
    print(short_term_memory(determine_tool("calculate the costs for a hotel with checkin date 27.03.2024, checkout date 10.04.2024 and a nightly cost of 235", tool_belt), "3290", 0))