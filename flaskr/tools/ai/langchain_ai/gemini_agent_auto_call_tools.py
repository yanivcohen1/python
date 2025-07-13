import os
import google.generativeai as genai
from google.generativeai import types

# --- Configuration ---
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

model = genai.GenerativeModel(
    model_name=model_name,
    tools=tools,
)

# Example with automatic function calling (simpler for many cases)
print("\n--- EXAMPLE WITH AUTOMATIC FUNCTION CALLING ---")
# In this mode, the SDK handles the calling of your registered Python functions
# based on the model's requests internally. You just get the final response.
# Your Python functions will still be executed, but you don't see the
# intermediate "MODEL wants to call function" and "PYTHON executed function"
# steps directly in this part of the code flow.
chat_auto = model.start_chat(enable_automatic_function_calling=True)
prompt_auto = (
    "What's the weather like in London, and what activity should I do based on that?"
)
print(f"USER: {prompt_auto}")
# ============== for none streaming (strean not supported) ==============
response_auto = chat_auto.send_message(prompt_auto)
# The automatic mode directly gives you the final text response after completing calls
print(f"MODEL (Final Text Response with Auto FC): {response_auto.text}")

# Note: With automatic function calling, the print statements inside your
# Python functions (`get_current_weather`, `suggest_activity`) will still run,
# showing that the functions were executed, but the control flow in your
# main script is simpler as you don't manually handle the function calls.
