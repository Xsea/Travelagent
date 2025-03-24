calculate_hotel_cost_tool_description = {
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

give_tourist_information_space_description = {
    "type": "function",
    "function": {
        "name": "answer_space_travel_questions",
        "description": """User Requests that search for information on travel location in Space (Luna, Mars or Massage)
                       can be answered here. This is used for general information of the surrounding area and cities. 
                       Information about the hotels can not be found here. 
                       Only use, if the information is not found in the context""",
        "parameters": {
            "type": "object",
            "properties": {
                "user_request": {
                    "type": "string",
                    "description": """the user request""",
                },
            },
            "required": ["user_request"],
            "additionalProperties": False,
        }
    }
}

list_hotels_description = {
    "type": "function",
    "function": {
        "name": "list_hotels",
        "description": """Given a planet (or moon), I will list only the names of all available hotels""",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": """the planet (Luna, Mars or Massage) for which you need the list of hotels""",
                    },
                },
            "required": ["location"],
            "additionalProperties": False,
        }
    }
}

give_hotel_information_description = {
    "type": "function",
    "function": {
        "name": "give_hotel_information",
        "description": """Given a Hotel Name, I will return all information regarding availability and prices""",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_name": {
                    "type": "string",
                    "description": """the name of the Hotel, for which you need the information""",
                    },
                },
            "required": ["hotel_name"],
            "additionalProperties": False,
        }
    }
}

collect_information_from_the_user_description = {
"type": "function",
    "function": {
        "name": "collect_information_from_the_user",
        "description": """I can ask the user a question, the answer will be returned to you""",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": """the question you want to ask the user""",
                    },
                },
            "required": ["question"],
            "additionalProperties": False,
        }
    }
}

book_hotel_description = {
"type": "function",
    "function": {
        "name": "book_hotel",
        "description": """Given all necessary information, I will book the travel, I will return a summary""",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_name": {
                    "type": "string",
                    "description": """the name of the Hotel, which I should book""",
                },
                "check_in": {
                    "type": "string",
                    "description": """the check_in date in format: yyyy-mm-dd""",
                },
                "check_out": {
                    "type": "string",
                    "description": """the check_in date in format: yyyy-mm-dd""",
                },
             },

            "required": ["hotel_name", "check_in", "check_out"],
            "additionalProperties": False,
        }
    }
}

book_flights_description = {
"type": "function",
    "function": {
        "name": "book_flights",
        "description": """Given all necessary information, I will book the flight, I will return a summary""",
        "parameters": {
            "type": "object",
            "properties": {
                "arrival_port": {
                    "type": "string",
                    "description": """the location of the arrival""",
                },
                "outbound_date": {
                    "type": "string",
                    "description": """the outbound flight date in format: yyyy-mm-dd""",
                },
                "return_date": {
                    "type": "string",
                    "description": """the return flight date in format: yyyy-mm-dd""",
                },
             },

            "required": ["arrival_port", "outbound_date", "return_date"],
            "additionalProperties": False,
        }
    }
}

