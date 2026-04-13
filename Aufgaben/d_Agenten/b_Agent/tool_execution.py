from Aufgaben.d_Agenten.tools_description import tool_belt
from tool_determination import determine_tool


def tool_execution(tool_call):
    # using the output of choices[0].message.tool_calls[0] object we now run the correct tool
    # write a big if/elif block that includes all tools. Check for tool.function.name
    # run the method with the correct arguments
    # for this use: arguments = json.loads(tool.function.arguments)
    # you can get the argument like this: arguments["start_date"]
    # return the output
    return ""


if __name__ == "__main__":
    print(tool_execution(determine_tool("calculate the costs for a hotel with checkin date 27.03.2024, checkout date 10.04.2024 and a nightly cost of 235", tool_belt)))
