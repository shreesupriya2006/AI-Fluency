"""
Day 6 - Structured Outputs Demo
Movie Booking Assistant
"""

from pathlib import Path
import sys

# Use Day 1 config.py
sys.path.append(str(Path(__file__).parent.parent / "day_1"))

from config import client,MODEL


QUESTION = """
Extract the movie booking details from this request:

I want 3 IMAX tickets for the movie tonight.
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "movie_type": {
            "type": "string",
            "enum": [
                "regular",
                "premium",
                "imax"
            ]
        },
        "number_of_tickets": {
            "type": "integer"
        }
    },
    "required": [
        "movie_type",
        "number_of_tickets"
    ],
    "additionalProperties": False
}


def no_constraint():
    print("\n" + "=" * 60)
    print("1. NO CONSTRAINT")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        temperature=0
    )

    print("RAW REPLY:")
    print(response.choices[0].message.content)


def json_mode():
    print("\n" + "=" * 60)
    print("2. JSON MODE")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON."
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        response_format={
            "type": "json_object"
        },
        temperature=0
    )

    raw=response.choices[0].message.content

    print("RAW REPLY:")
    print(raw)

    try:
        import json
        parsed=json.loads(raw)

        print("PARSED RESULT:")
        print(parsed)

    except Exception as error:
        print("PARSE ERROR:",error)


def schema_mode():
    print("\n" + "=" * 60)
    print("3. JSON SCHEMA MODE")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract the requested movie booking details."
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "movie_booking",
                "strict": True,
                "schema": SCHEMA
            }
        },
        temperature=0
    )

    raw=response.choices[0].message.content

    print("RAW REPLY:")
    print(raw)

    try:
        import json
        parsed=json.loads(raw)

        print("PARSED RESULT:")
        print(parsed)

    except Exception as error:
        print("PARSE ERROR:",error)


if __name__ == "__main__":

    print("MOVIE BOOKING - STRUCTURED OUTPUTS")

    no_constraint()
    json_mode()
    schema_mode()