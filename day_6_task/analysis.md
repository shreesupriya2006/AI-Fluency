# Day 6 Analysis

## 1. Chat Completions

Chat Completions uses a request containing a model and a list of messages.

Important request fields:

* `model` – specifies the model to use.
* `messages` – contains system, user, assistant, and tool messages.
* `tools` – defines functions that the model can request.
* `temperature` – controls randomness.
* `max_tokens` – limits generated output.

Important response fields:

* `message.content` – normal model response.
* `message.tool_calls` – tools requested by the model.
* `finish_reason` – explains why generation stopped.

Common `finish_reason` values:

* `stop` – normal completion.
* `length` – token limit reached.
* `tool_calls` – model requested tool calls.

## 2. OpenAI-Compatible Servers

An OpenAI-compatible server provides an API with an interface similar to the OpenAI API. This allows applications to use different model providers with similar client code by changing configuration such as the base URL and model.

## 3. Streaming

Streaming sends the model response in smaller pieces while it is being generated instead of waiting for the complete response. It improves responsiveness in applications such as chat interfaces.

## 4. Responses API vs Chat Completions

Chat Completions uses a messages-based interface and supports tool calling. The Responses API is another API interface designed for model responses and tool-based applications.

This project uses Chat Completions.

## 5. Five Steps of Tool Calling

1. The user sends a request.
2. The model decides that a tool is required and generates a tool call.
3. The application receives the tool call.
4. The application validates and executes the function.
5. The tool result is sent back to the model, which produces the final response.

The LLM does not directly execute the Python function. The application executes it.

## 6. Tool Definition

A tool definition contains:

* Tool type
* Function name
* Description
* Parameters
* JSON Schema for the parameters

`tool_choice` can control whether the model automatically chooses a tool or whether a specific tool/use behavior is required.

## 7. JSON Mode vs JSON Schema Mode

**JSON mode** ensures that the model produces valid JSON, but it does not necessarily restrict the exact fields or values.

**JSON Schema mode** defines the required structure, field types, allowed values, and additional-property rules.

In this project, schema mode produced:

```json
{
  "movie_type": "imax",
  "number_of_tickets": 3
}
```

## 8. Parallel Tool Calls

A model may request multiple independent tools in one response. The application should process every tool call and return one tool message for each `tool_call_id`.

## 9. Tool Failures

Tool failures should not crash the agent. The failure should be converted into a string and returned to the model so that the model can respond or retry appropriately.

Examples:

* Invalid JSON
* Unknown tool
* Missing argument
* Extra argument
* Wrong argument type
* Invalid enum value
* Tool execution error

## 10. Repair and Retry Pattern

When a tool call fails, the application can return the error to the model. The model can then generate a corrected tool call.

The agent should also have limits such as:

* Maximum number of steps
* Maximum repeated identical calls
* Token retry limits

This prevents infinite loops.

## 11. Fault Injection

Fault injection deliberately sends broken tool calls to test whether validation works correctly.

The Movie Booking fault-injection script tests:

* Missing arguments
* Wrong types
* Invalid enum values
* Extra arguments
* Unknown tools
* Invalid ticket counts

## 12. Tool Calling vs Structured Outputs

| Tool Calling                                   | Structured Outputs                                    |
| ---------------------------------------------- | ----------------------------------------------------- |
| Used when the model needs to request an action | Used when the model needs a specific output structure |
| Application executes the requested function    | Application receives structured data                  |
| Example: calculate ticket price                | Example: extract movie type and ticket count          |
| Requires tool execution and tool results       | Does not require executing a tool                     |
| Can involve multiple tool calls                | Produces data matching a defined schema               |

## 13. Project Scenario

The project implements a Movie Booking Assistant.

Tools:

1. `get_ticket_price(movie_type)`
2. `calculate_total_price(price, number_of_tickets)`

The tools use JSON Schema validation before execution.

The agent also handles invalid arguments, repeated calls, token-limit retries, multiple tool calls, and maximum-step limits.
