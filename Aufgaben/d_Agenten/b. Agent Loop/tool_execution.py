def tool_execution(tool):
    # using the output of choices[0].message.tool_calls[0] object we now run the correct tool
    # write a big if/elif block that includes all tools. Check for tool.function.name
    # run the method with the correct arguments
    # for this use: arguments = json.loads(tool.function.arguments)
    # return the output

## TODO write a dummy call on a tool (use output from tool_determination)