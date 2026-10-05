"""
Day 6 - Fault Injection
Movie Booking Assistant
"""

import json

from tools_v2 import SCHEMAS
from validate import validate_arguments


def test_fault(tool_name,arguments,description):
    print("\n" + "=" * 60)
    print("FAULT:",description)
    print("TOOL:",tool_name)
    print("ARGS:",arguments)

    schema=SCHEMAS.get(tool_name)

    if schema is None:
        print("RESULT: Unknown tool")
        return

    problem=validate_arguments(arguments,schema)

    if problem:
        print("RESULT: REJECTED")
        print("REASON:",problem)
    else:
        print("RESULT: ACCEPTED")


faults=[
    (
        "get_ticket_price",
        {},
        "Missing required argument"
    ),

    (
        "get_ticket_price",
        {"movie_type":"3D"},
        "Invalid enum value"
    ),

    (
        "get_ticket_price",
        {"movie_type":123},
        "Wrong argument type"
    ),

    (
        "get_ticket_price",
        {
            "movie_type":"imax",
            "extra":"hack"
        },
        "Extra unexpected argument"
    ),

    (
        "calculate_total_price",
        {"price":350},
        "Missing number_of_tickets"
    ),

    (
        "calculate_total_price",
        {
            "price":"350",
            "number_of_tickets":2
        },
        "Wrong price type"
    ),

    (
        "calculate_total_price",
        {
            "price":350,
            "number_of_tickets":"two"
        },
        "Wrong ticket count type"
    ),

    (
        "calculate_total_price",
        {
            "price":350,
            "number_of_tickets":2,
            "discount":50
        },
        "Extra discount argument"
    ),

    (
        "calculate_total_price",
        {
            "price":350,
            "number_of_tickets":2.5
        },
        "Non-integer ticket count"
    ),

    (
        "unknown_tool",
        {"movie_type":"imax"},
        "Unknown tool"
    )
]


print("MOVIE BOOKING - FAULT INJECTION")

for tool_name,arguments,description in faults:
    test_fault(
        tool_name,
        arguments,
        description
    )

print("\n" + "=" * 60)
print("Fault injection completed.")