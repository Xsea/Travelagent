import json
from Solutions.d_Agenten.tools_description import tool_belt
from Solutions.d_Agenten.b_Agent.tool_determination import determine_tool
from Solutions.d_Agenten.tools import give_tourist_information_space, calculate_hotel_cost, list_hotels,\
    give_hotel_information, collect_information_from_the_user, book_hotel, book_flights


def tool_execution(tool_call):
    arguments = json.loads(tool_call.function.arguments)
    output = ""
    try:
        if tool_call.function.name == "calculate_hotel_cost":
            output = calculate_hotel_cost(arguments["start_date"], arguments["end_date"], arguments["price"])
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
            output = book_flights(
                arguments["arrival_port"], arguments["outbound_date"], arguments["return_date"]
                )
    except Exception as error:
        output = f"error while calling {tool_call.function.name} with arguments {arguments}. Error Message: {error}"
    return output

if __name__ == "__main__":
    print(tool_execution(determine_tool("calculate the costs for a hotel with checkin date 27.03.2024, checkout date 10.04.2024 and a nightly cost of 235", tool_belt)))