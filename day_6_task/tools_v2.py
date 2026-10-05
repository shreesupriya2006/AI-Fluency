"""
Day 6 - Movie Booking Assistant
Tools and JSON schemas
"""

TICKET_PRICES = {
    "regular": 180,
    "premium": 250,
    "imax": 350
}


def get_ticket_price(movie_type):
    if movie_type not in TICKET_PRICES:
        valid_types = ", ".join(TICKET_PRICES.keys())
        return f"Unknown movie type: {movie_type}. Valid types: {valid_types}."

    return TICKET_PRICES[movie_type]


def calculate_total_price(price,number_of_tickets):
    return price*number_of_tickets


SCHEMAS = {
    "get_ticket_price": {
        "type": "object",
        "properties": {
            "movie_type": {
                "type": "string",
                "enum": [
                    "regular",
                    "premium",
                    "imax"
                ]
            }
        },
        "required": [
            "movie_type"
        ],
        "additionalProperties": False
    },

    "calculate_total_price": {
        "type": "object",
        "properties": {
            "price": {
                "type": "number"
            },
            "number_of_tickets": {
                "type": "integer"
            }
        },
        "required": [
            "price",
            "number_of_tickets"
        ],
        "additionalProperties": False
    }
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_price",
            "description": "Get the ticket price for a movie type.",
            "parameters": SCHEMAS["get_ticket_price"]
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_total_price",
            "description": "Calculate the total price for movie tickets.",
            "parameters": SCHEMAS["calculate_total_price"]
        }
    }
]


TOOL_FUNCTIONS = {
    "get_ticket_price": get_ticket_price,
    "calculate_total_price": calculate_total_price
}