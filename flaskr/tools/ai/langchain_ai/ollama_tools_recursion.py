import ollama
import json
import math # For safe evaluation if needed

# --- Configuration ---
MAX_ITERATIONS = 5
MODEL_NAME = 'qwen3:1.7b' # Make sure you have pulled this model

# --- 1. Define Tool Functions ---

def get_current_weather(location: str, unit: str = "celsius"):
    """Gets the current weather for a specified location. Returns JSON."""
    print(f"--- Tool Func [Weather]: location='{location}', unit='{unit}' ---")
    # Simulate fetching weather data
    weather_data = {}
    if "tokyo" in location.lower():
        weather_data = {"location": location, "temperature": "15", "unit": unit, "forecast": "cloudy"}
    elif "london" in location.lower():
        weather_data = {"location": location, "temperature": "10", "unit": unit, "forecast": "rainy"}
    elif "ottawa" in location.lower():
        weather_data = {"location": location, "temperature": "3", "unit": unit, "forecast": "snowy"}
    elif "paris" in location.lower():
        weather_data = {"location": location, "temperature": "12", "unit": unit, "forecast": "partly cloudy"}
    else:
        weather_data = {"Error": "Location not found"}
    return json.dumps(weather_data)

def calculate(expression: str):
    """Evaluates a simple mathematical expression. Returns JSON."""
    print(f"--- Tool Func [Calculate]: expression='{expression}' ---")
    # SECURITY WARNING: eval() is insecure. Use a safer method in production.
    try:
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Expression contains invalid characters.")
        result = eval(expression, {"__builtins__": None}, {})
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        print(f"Error evaluating expression '{expression}': {e}")


        return json.dumps({"expression": expression, "error": str(e) + " prehaps you inserted a variable in the expression?"})

def get_capital(country: str):
    """Gets the capital city of a given country. Returns JSON."""
    print(f"--- Tool Func [Capital]: country='{country}' ---")
    capitals = {
        "france": "Paris",
        "canada": "Ottawa",
        "japan": "Tokyo",
        "uk": "London",
        "usa": "Washington D.C."
    }
    capital = capitals.get(country.lower(), "Unknown")
    if capital == "Unknown":
        return json.dumps({"country": country, "error": "Capital not found in database"})
    else:
        return json.dumps({"country": country, "capital": capital})

# Map tool names to functions
available_tools = {
    "get_current_weather": get_current_weather,
    "calculate": calculate,
    "get_capital": get_capital,
}

# --- 2. Define Tool Schemas ---
tools_schema = [
    {
        'type': 'function',
        'function': {
            'name': 'get_current_weather',
            'description': 'Gets the current weather for a specified location. Returns JSON.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string',
                        'description': 'The city and state/country (e.g., "San Francisco, CA")',
                    },
                    'unit': {
                        'type': 'string',
                        'enum': ['celsius', 'fahrenheit'],
                        'description': 'The temperature unit to use.'
                    },
                },
                'required': ['location'],
            },
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'calculate',
            'description': 'Evaluates a simple mathematical expression (python eval syntax without variables). Returns JSON.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'expression': {
                        'type': 'string',
                        'description': 'The mathematical expression to evaluate. (python eval syntax without variables)',
                    },
                },
                'required': ['expression'],
            },
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_capital',
            'description': 'Gets the capital city of a given country. Returns JSON.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'country': {
                        'type': 'string',
                        'description': 'The country for which to find the capital (e.g., "Canada").',
                    },
                },
                'required': ['country'],
            },
        }
    }
]

# --- 3. Initialize Client and Messages ---
client = ollama.Client()

# Prompt designed to potentially require multiple steps
# query = 'What is the capital of Canada, and what is the weather like in Celsius at this capital and multiply capital temperature in 10?'
query = 'first step find the weather in Ottawa in Celsius, second step calculate the convertion to Fahrenheit?'
messages = [
    {'role': 'user', 'content': query},
    {'role': 'system', 'content': 'You are a helpful assistant that can call tools to get information, all calculation will be with calculate tool.'},
]
print(f"Initial User Prompt: {messages[-1]['content']}\n")

# --- 4. Iterative Tool Call Loop ---
final_answer_message = None
current_iteration = 0
for i in range(MAX_ITERATIONS):
    print(f"\n--- Iteration {i + 1} ---")
    current_iteration = i
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=tools_schema,
        )
        response_message = response['message']
        messages.append(response_message) # Append assistant's response/request

        # Check if the model wants to call tools
        if not response_message.get('tool_calls'):
            print("Model finished. No more tool calls requested.")
            final_answer_message = response_message # This is the final answer
            break # Exit the loop

        # --- Process Tool Calls ---
        print(f"\nTool Calls Requested: {len(response_message['tool_calls'])}")
        tool_calls_pending = response_message['tool_calls']

        # Execute all requested tools
        for tool_call in tool_calls_pending:
            function_name = tool_call['function']['name']
            function_args_str = tool_call['function']['arguments']
            tool_call_id = tool_call.get('id') # Get ID if available/needed

            print(f"  - Tool: {function_name}, Args: {function_args_str}")

            if function_name in available_tools:
                tool_function = available_tools[function_name]
                try:
                    # Decode arguments
                    # args = json.loads(function_args_str)

                    # Execute function
                    tool_output = tool_function(**function_args_str)

                    print(f"    Output: {tool_output}")

                    # Append tool result message
                    messages.append({
                        'role': 'tool',
                        'content': tool_output,
                        # Include 'tool_call_id': tool_call_id if required by your Ollama setup/model
                    })

                except json.JSONDecodeError:
                    print(f"    Error: Could not decode JSON arguments: {function_args_str}")
                    messages.append({'role': 'tool', 'content': json.dumps({"error": "Invalid JSON arguments received"})})
                except Exception as e:
                    print(f"    Error executing tool {function_name}: {e}")
                    messages.append({'role': 'tool', 'content': json.dumps({"error": f"Failed to execute tool: {e}"})})
            else:
                print(f"  Error: Unknown tool '{function_name}' requested.")
                messages.append({'role': 'tool', 'content': json.dumps({"error": f"Unknown tool '{function_name}' requested"})})

        # Check if loop is about to end due to iteration limit
        if i == MAX_ITERATIONS - 1:
            print(f"\n--- Max iterations ({MAX_ITERATIONS}) reached. ---")
            # The last message from the assistant might have been another tool request
            # or potentially an answer based on the final tool calls.
            # We don't make another call, the last assistant message is the final state.
            final_answer_message = response_message
            break

    except Exception as e:
        print(f"\nAn error occurred during API call or processing: {e}")
        print("Ensure Ollama server is running and model is available.")
        final_answer_message = {'role': 'assistant', 'content': f"An error occurred: {e}"}
        break

if current_iteration == MAX_ITERATIONS - 1:
    print("\n--- Max iterations reached. Final answer may be incomplete. ---")

# --- 5. Print Final Result ---
# print("\n--- Final Conversation History ---")
# for msg in messages:
#     role = msg.get('role', 'unknown')
#     content = msg.get('content', '')
#     tool_calls = msg.get('tool_calls') # This is the list of ToolCall-like objects/dicts

#     print(f"[{role.upper()}]")
#     if content:
#         print(content)
#     if tool_calls:
#         # Convert tool_calls to a JSON-serializable format (list of dicts)
#         serializable_tool_calls = []
#         for tc in tool_calls:
#             # Assuming tc behaves like a dictionary or has accessible attributes
#             # Adjust keys ('id', 'type', 'function') if library representation differs
#             serializable_call = {
#                 "id": tc.get("id") if isinstance(tc, dict) else getattr(tc, 'id', None), # Handle dict or object access
#                 "type": tc.get("type", "function") if isinstance(tc, dict) else getattr(tc, 'type', 'function'),
#                 "function": {
#                     "name": tc.get("function", {}).get("name") if isinstance(tc, dict) else getattr(getattr(tc, 'function', {}), 'name', None),
#                     "arguments": tc.get("function", {}).get("arguments") if isinstance(tc, dict) else getattr(getattr(tc, 'function', {}), 'arguments', None)
#                 }
#             }
#             # Clean up None values if desired, though json.dumps handles them
#             serializable_call = {k: v for k, v in serializable_call.items() if v is not None}
#             if 'function' in serializable_call:
#                 serializable_call['function'] = {k: v for k, v in serializable_call['function'].items() if v is not None}

#             serializable_tool_calls.append(serializable_call)

#         try:
#             # Now dump the serializable list
#             print(f"  Tool Calls: {json.dumps(serializable_tool_calls, indent=2)}")
#         except TypeError as e:
#             # Fallback if conversion still fails
#             print(f"  Tool Calls (raw representation, JSON failed: {e}): {tool_calls}")


print("\n--- Final Assistant Answer ---")
# (Rest of the final answer printing logic remains the same)
# ...
if final_answer_message and final_answer_message.get('content'):
    print(final_answer_message['content'])
elif final_answer_message and final_answer_message.get('tool_calls'):
    print("(Process ended with the model requesting further tool calls due to iteration limit)")
elif not final_answer_message and messages and messages[-1]['role'] == 'assistant':
    # Fallback if loop ended abruptly but last message was assistant
    print(messages[-1]['content'])
else:
    print("(Could not determine final answer)")
