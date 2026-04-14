"""JSON schemas for the agent tools — one per function in tools.py."""

calculate_hotel_cost_tool_description = {
    "type": "function",
    "function": {
        "name": "calculate_hotel_cost",
        "description": "Given a start date, end date and nightly price, calculate the total stay cost.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Check-in date in format yyyy-mm-dd",
                },
                "end_date": {
                    "type": "string",
                    "description": "Check-out date in format yyyy-mm-dd",
                },
                "price": {
                    "type": "number",
                    "description": "The nightly cost of the hotel in €",
                },
            },
            "required": ["start_date", "end_date", "price"],
            "additionalProperties": False,
        },
    },
}

list_hotels_description = {
    "type": "function",
    "function": {
        "name": "list_hotels",
        "description": "Given a planet or moon, list the names of all available hotels there.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The destination (Luna, Mars, or Massage)",
                },
            },
            "required": ["location"],
            "additionalProperties": False,
        },
    },
}

give_hotel_information_description = {
    "type": "function",
    "function": {
        "name": "give_hotel_information",
        "description": "Given a hotel name, return its price per night and available date ranges.",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_name": {
                    "type": "string",
                    "description": "The name of the hotel",
                },
            },
            "required": ["hotel_name"],
            "additionalProperties": False,
        },
    },
}

book_hotel_description = {
    "type": "function",
    "function": {
        "name": "book_hotel",
        "description": "Book a hotel for a given date range. Returns a confirmation with the total cost.",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_name": {
                    "type": "string",
                    "description": "The name of the hotel to book",
                },
                "check_in": {
                    "type": "string",
                    "description": "Check-in date in format yyyy-mm-dd",
                },
                "check_out": {
                    "type": "string",
                    "description": "Check-out date in format yyyy-mm-dd",
                },
            },
            "required": ["hotel_name", "check_in", "check_out"],
            "additionalProperties": False,
        },
    },
}

give_tourist_information_space_description = {
    "type": "function",
    "function": {
        "name": "give_tourist_information_space",
        "description": (
            "Answer general tourist questions about space destinations (Luna, Mars, Massage) using RAG. "
            "Use this for sights, activities, and atmosphere — NOT for hotel listings or prices."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "user_request": {
                    "type": "string",
                    "description": "The user's question, in natural language",
                },
            },
            "required": ["user_request"],
            "additionalProperties": False,
        },
    },
}
