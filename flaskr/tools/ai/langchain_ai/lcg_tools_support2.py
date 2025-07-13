from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama
from langchain.schema import HumanMessage

# load_dotenv()

# @tool
def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """
    Get the current weather in a given location.

    Args:
        location (str): The city and state, e.g., "San Francisco, CA" or a zip code.
        unit (str): The temperature unit, either "celsius" or "fahrenheit". Defaults to "celsius".

    Returns:
        dict: A dictionary containing the location, temperature, unit, and a brief forecast.
    """
    print(f"\nPYTHON: Called get_current_weather(location='{location}', unit='{unit}')")
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

    ansr = {
        "location": location,
        "temperature": temp,
        "unit": unit,
        "forecast": forecast,
    }
    print("get_current_weather Answer:", ansr)
    return ansr

# @tool
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
        f"\nPYTHON: Called suggest_activity(weather_forecast='{weather_forecast}', temperature='{temperature}', unit='{unit}')"
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

    ansr = {
        "weather_forecast": weather_forecast,
        "temperature": temperature,
        "unit": unit,
        "suggested_activity": suggestion,
    }
    print("Suggest_activity Answer:", ansr)
    return ansr

if __name__ == "__main__":
    model = ChatOllama(model="qwen3:1.7b")
    tools = [get_current_weather, suggest_activity]
    agent = create_react_agent(model, tools)
    query = "What's the weather like in London, and what activity should I do based on that?"
    # 5. Invoke the agent
    while True:
        user_input = input("\nYou: ").strip()
        if user_input == "quit":
            break
        if user_input == "":
            user_input = query
            print("Using default query:", user_input)
        print("\nAssistant: ", end="")
        for chunk in agent.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk ["agent"]["messages"]:
                    print(message.content, end="")
        print()


    # for chunk in agent.stream({
    #     "messages": [("user", query),("system", "Please answer in a step-by-step manner. use only the tools you have,\
    #                                   all calculation will be only with Calculator tool\
    #                                   all weather information will be only with Weather tool")],
    # }, stream_mode="messages"):
    #     if chunk[0].content:
    #         print(chunk[1]["langgraph_node"],':', chunk[0].name, "-", chunk[0].content, end="\n")
