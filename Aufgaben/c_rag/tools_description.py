calculate_hotel_cost_tool = {
    "type": "function",
    "function": {
        "name": "calculate_hotel_cost",
        "description": "Given a start and end date, I will be able to calculate how much the stay at the hotel costs",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": """The day the person arrives for their hotel stay. Given in format yyyy-mm-dd""",
                },
                "end_date": {
                    "type": "string",
                    "description": """The day the person leaves the hotel. Given in format yyyy-mm-dd""",
                },
            },
            "required": ["start_date", "end_date"],
            "additionalProperties": False,
        }
    }
}

# add space travel tool here