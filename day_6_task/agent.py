"""
Day 6 - Reliable Movie Booking Agent
"""

import json
import sys
from pathlib import Path

# Use Day 1 config.py
sys.path.append(str(Path(__file__).parent.parent / "day_1"))

from config import client,MODEL,banner
from tools_v2 import TOOLS,TOOL_FUNCTIONS,SCHEMAS
from validate import validate_arguments


SYSTEM_PROMPT = (
    "You are a movie booking assistant. "
    "Use get_ticket_price to find ticket prices. "
    "Use calculate_total_price to calculate the total cost. "
    "Never guess a ticket price when the tool can provide it. "
    "Valid movie types are regular, premium, and imax. "
    "If no tool is needed, answer directly."
)


MAX_TOKENS = 300
REPEAT_LIMIT = 3


def handle_tool_call(call,log=True):
    """
    Safely process one tool call.
    Every failure is returned as a string instead of crashing.
    """

    name = call.function.name
    raw = call.function.arguments or "{}"

    # Stage 1: Parse JSON
    try:
        arguments = json.loads(raw)
    except json.JSONDecodeError as error:
        return (
            f"Argument error: invalid JSON ({error}). "
            f"Send valid JSON for '{name}'."
        )

    # Stage 2: Find the tool
    function = TOOL_FUNCTIONS.get(name)

    if function is None:
        return (
            f"Unknown tool: {name}. "
            f"Available tools: {', '.join(TOOL_FUNCTIONS)}."
        )

    # Stage 3: Validate arguments
    problem = validate_arguments(
        arguments,
        SCHEMAS[name]
    )

    if problem:
        return f"Argument error: {problem}"

    # Stage 4: Execute the tool
    try:
        result = str(function(**arguments))
    except Exception as error:
        result = (
            f"Tool error in {name}: "
            f"{type(error).__name__}: {error}"
        )

    if log:
        print(
            f"      {name}({arguments}) -> {result}"
        )

    return result


def agent(question,max_steps=6,verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    seen = {}
    max_tokens = MAX_TOKENS

    for step in range(1,max_steps+1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0,
            max_tokens=max_tokens
        )

        choice = response.choices[0]
        message = choice.message

        # Handle truncated response
        if choice.finish_reason == "length":

            if max_tokens >= 2000:
                return (
                    "Stopped: the reply was still "
                    "truncated at 2000 tokens."
                )

            max_tokens *= 2

            if verbose:
                print(
                    f"   step {step}: truncated, "
                    f"retrying with max_tokens={max_tokens}"
                )

            continue

        # No tool call -> final answer
        if not message.tool_calls:
            return (message.content or "").strip()

        # Add assistant tool-call message
        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in message.tool_calls
                ]
            }
        )

        if verbose:
            print(
                f"   step {step}: "
                f"{len(message.tool_calls)} tool call(s)"
            )

        # Process every tool call
        for call in message.tool_calls:

            signature = (
                call.function.name,
                call.function.arguments
            )

            seen[signature] = seen.get(signature,0) + 1

            # Stop repeated identical calls
            if seen[signature] >= REPEAT_LIMIT:
                return (
                    f"Stopped: {call.function.name} "
                    f"was called {REPEAT_LIMIT} times "
                    f"with the same arguments and made no progress."
                )

            result = handle_tool_call(
                call,
                log=verbose
            )

            # Send result back to model
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                }
            )

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


if __name__ == "__main__":

    banner("MOVIE BOOKING AGENT")

    questions = [
        "How much does one premium movie ticket cost?",
        "How much will 3 IMAX tickets cost?",
        "How much will 2 regular tickets cost?",
        "What is the difference between one regular and one IMAX ticket?",
        "Write a short welcome message for a movie booking app."
    ]

    for question in questions:

        print("\nQ:",question)

        answer = agent(question)

        print("A:",answer)