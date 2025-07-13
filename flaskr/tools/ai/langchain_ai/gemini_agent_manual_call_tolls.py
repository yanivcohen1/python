import json
import os
import google.generativeai as genai
from google.generativeai import types

# --- Configuration ---
# Set your API key as an environment variable or directly here.
# It's recommended to use environment variables for security.
# os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# For this example, let's use a placeholder if the API key is not set.
# In a real application, you MUST provide a valid API key.

# try:
#     # Attempt to configure with an environment variable if available
#     api_key = os.environ.get("GEMINI_API_KEY")
#     if not api_key:
#         # Fallback to a placeholder if env var is not set
#         print("GEMINI_API_KEY environment variable not found.")
#         print(
#             "Using a placeholder API key for demonstration purposes. This will likely fail to connect to the API."
#         )
#         api_key = "YOUR_API_KEY_PLACEHOLDER"

#     genai.configure(api_key=api_key)

# except Exception as e:
#     print(f"Configuration failed: {e}")

try:
    # Attempt to configure with an environment variable if available
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Fallback to a placeholder if env var is not set
        print("GEMINI_API_KEY environment variable not found.")
        print(
            "Using a placeholder API key for demonstration purposes. This will likely fail to connect to the API."
        )

    genai.configure(api_key=api_key)

except Exception as e:
    print(f"Configuration failed: {e}")

# --- 1. Define your functions that the model can call ---


def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """
    Get the current weather in a given location.

    Args:
        location (str): The city and state, e.g., "San Francisco, CA" or a zip code.
        unit (str): The temperature unit, either "celsius" or "fahrenheit". Defaults to "celsius".

    Returns:
        dict: A dictionary containing the location, temperature, unit, and a brief forecast.
    """
    print(f"PYTHON: Called get_current_weather(location='{location}', unit='{unit}')")
    # In a real application, you would call a weather API here.
    # For this example, we'll return mock data.
    lower_location = location.lower()
    if "tokyo" in lower_location:
        temp = "15" if unit == "celsius" else "59"
        forecast = "Cloudy with a chance of rain."
    elif "london" in lower_location:
        temp = "10" if unit == "celsius" else "50"
        forecast = "Mostly sunny."
    elif "new york" in lower_location:
        temp = "5" if unit == "celsius" else "41"
        forecast = "Snowy."
    else:
        temp = "22" if unit == "celsius" else "72"
        forecast = "Pleasant weather."

    return {
        "location": location,
        "temperature": temp,
        "unit": unit,
        "forecast": forecast,
    }


def suggest_activity(weather_forecast: str, temperature: str, unit: str) -> dict:
    """
    Suggests an activity based on the current weather forecast and temperature.

    Args:
        weather_forecast (str): The current weather conditions (e.g., "Cloudy with a chance of rain.").
        temperature (str): The current temperature as a string (e.g., "15").
        unit (str): The temperature unit ("celsius" or "fahrenheit").

    Returns:
        dict: A dictionary containing the weather information and the suggested activity.
    """
    print(
        f"PYTHON: Called suggest_activity(weather_forecast='{weather_forecast}', temperature='{temperature}', unit='{unit}')"
    )

    temp_val = int(
        temperature
    )  # Assuming temperature is always a valid integer string in mock data

    suggestion = "It's hard to suggest an activity with this weather information."

    if "rain" in weather_forecast.lower() or "cloudy" in weather_forecast.lower():
        suggestion = "It might be good to stay indoors. How about reading a book or watching a movie?"
    elif "sunny" in weather_forecast.lower() or "pleasant" in weather_forecast.lower():
        if (unit == "celsius" and temp_val > 18) or (
            unit == "fahrenheit" and temp_val > 65
        ):
            suggestion = "The weather seems nice for outdoor activities! How about a walk in the park?"
        else:
            suggestion = (
                "It's a bit cool but sunny. Maybe a brisk walk or visiting a museum?"
            )
    elif "snow" in weather_forecast.lower():
        suggestion = "It's snowy! Perfect weather for staying cozy inside or maybe trying some winter sports if possible!"

    return {
        "weather_forecast": weather_forecast,
        "temperature": temperature,
        "unit": unit,
        "suggested_activity": suggestion,
    }


# --- 2. Initialize the Generative Model with tools ---

model_name = (
    "gemini-2.0-flash-thinking-exp"  # Using a model expected to support tool use
)

# Create a list of tools from your Python functions.
tools = [get_current_weather, suggest_activity]

# Create a dictionary mapping function names (as strings) to the actual Python functions.
# This is used by the manual function calling loop to find and execute the function.
available_tools = {
    "get_current_weather": get_current_weather,
    "suggest_activity": suggest_activity,
}

model = genai.GenerativeModel(
    model_name=model_name,
    tools=tools,
)

# --- 3. Start a chat session ---
# Disable automatic calling for manual demonstration of the sequence.
chat = model.start_chat(enable_automatic_function_calling=False)

# --- 4. Send a prompt that requires sequential function calls ---
# The prompt asks for weather AND an activity based on it,
# guiding the model to understand the dependency.
prompt = "What's the weather like in London, and what activity should I do based on that?"
print(f"USER: {prompt}")

response = chat.send_message(prompt)
print(f"MODEL (Initial Response Parts): {response.parts}")

# --- 5. Process the model's response for function calls in a loop ---

# This loop continues as long as the model responds with a function call.
# This allows handling sequences of tool calls.
while (
    response.candidates
    and response.candidates[0].content.parts
    and response.candidates[0].content.parts[0].function_call
):
    function_call_part = response.candidates[0].content.parts[0]
    fc = function_call_part.function_call
    function_name = fc.name
    # Convert the function call arguments to a standard dictionary
    function_args = dict(fc.args) if fc.args else {}

    print(
        f"MODEL: Wants to call function '{function_name}' with arguments: {function_args}"
    )

    # --- 6. Execute the function if it's one you've defined ---
    if function_name in available_tools:
        tool_function = available_tools[function_name]

        try:
            # Call the Python function with the arguments provided by the model
            api_response_data = tool_function(**function_args)

            # --- 7. Send the function's result back to the model ---
            print(f"PYTHON: Executed '{function_name}'. Result: {api_response_data}")

            # Construct the FunctionResponse part. The response needs to be nested under 'content'.
            function_response_part = {
                "name": function_name,
                "response": {"content": api_response_data}
            }

            # Send the function response back to the model to continue the conversation
            response = chat.send_message(function_response_part)
            print(f"MODEL (After Function Result Parts): {response.parts}")

        except Exception as e:
            print(f"ERROR: Failed to execute function '{function_name}': {e}")
            error_response_part = {
                "name": function_name,
                "response": {"error": f"Execution failed: {e}"}
            }
            error_response_txt = json.dumps(error_response_part)
            response = chat.send_message(error_response_txt)
            print(f"MODEL (After Error Parts): {response.parts}")
            break  # Exit loop on error

    else:
        error_response_part = {
            "name": function_name,
            "response": {"error": f"Unknown function: {function_name}"}
        }
        error_response_txt = json.dumps(error_response_part)
        # name=function_name, response={"error": f"Unknown function: {function_name}"}
        response = chat.send_message(error_response_txt)
        print(f"MODEL (After Error Parts): {response.parts}")
        break  # Exit loop if function is unknown

# --- 8. Get the final response from the model ---
# After all function calls are resolved (or if no function call was made initially),
# the model will provide a final textual response summarizing the results.
# Check if the last response contains text parts
final_response_text = "".join(
    part.text for part in response.parts if hasattr(part, "text") and part.text
)

if final_response_text:
    print(f"MODEL (Final Text Response): {final_response_text}")
else:
    # This might happen if the last interaction was a function call/response
    # without a final text response, or if there was an error.
    print("MODEL: Did not provide a final text response after function calls.")
    # You might inspect response.candidates here for more details if needed.


# Example with automatic function calling (simpler for many cases)
print("\n--- EXAMPLE WITH AUTOMATIC FUNCTION CALLING ---")
# In this mode, the SDK handles the calling of your registered Python functions
# based on the model's requests internally. You just get the final response.
# Your Python functions will still be executed, but you don't see the
# intermediate "MODEL wants to call function" and "PYTHON executed function"
# steps directly in this part of the code flow.
chat_auto = model.start_chat(enable_automatic_function_calling=True)
prompt_auto = (prompt)
print(f"USER: {prompt_auto}")
# ============== for none streaming ==============
response_auto = chat_auto.send_message(prompt_auto)
# The automatic mode directly gives you the final text response after completing calls
print(f"MODEL (Final Text Response with Auto FC): {response_auto.text}")

# ============== for streaming not supported ==============
# Use stream=True to get a streamed response
# response_auto_stream = chat_auto.send_message(prompt_auto, stream=True)
# print(f"MODEL (Streamed Final Text Response with Auto FC): ", end="")
# # Iterate over the streamed response parts and print the text as it arrives
# # The functions (get_current_weather, suggest_activity) will be called
# # automatically by the SDK during this streaming process.
# try:
#     for chunk in response_auto_stream:
#         # Check if the chunk has text content and print it
#         if chunk.text:
#             print(chunk.text, end="")
#     print("\n") # Add a newline at the end
# except Exception as e:
#     print(f"\nAn error occurred during streaming: {e}")

# Note: With automatic function calling, the print statements inside your
# Python functions (`get_current_weather`, `suggest_activity`) will still run,
# showing that the functions were executed, but the control flow in your
# main script is simpler as you don't manually handle the function calls.
