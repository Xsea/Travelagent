calculate_hotel_cost_tool = {
    "type": "function",
    "function": {
        # add name and description. Remember, the LLM reads this info and uses this information to determine when and how to use it
        "name": "name",
        "description": "description",
        "parameters": {
            "type": "object",
            "properties": {
                # properties have the format:
                # "name": {
                #    "type": "string, number, boolean....",
                #    "description": the description of this parameter, so the LLM knows what it is for, and how to get it from the user request,
                #},
            },
            # required takes the name of the parameters
            "required": [],
            "additionalProperties": False,
        }
    }
}