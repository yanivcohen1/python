import os
import json
from typing import TypedDict

from dotenv import load_dotenv
# from imap_tools import MailBox, AND

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END

# load_dotenv()

# IMAP_HOST = os.getenv('IMAP_HOST')
# IMAP_USER = os.getenv('IMAP_USER')
# IMAP_PASSWORD = os.getenv('IMAP_PASSWORD')
# IMAP_FOLDER = 'INBOX'

CHAT_MODEL = 'qwen3:1.7b'


class ChatState(TypedDict):
    messages: list


@tool
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

@tool
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



llm = init_chat_model(CHAT_MODEL, model_provider='ollama')
llm = llm.bind_tools([get_current_weather, suggest_activity])

raw_llm = init_chat_model(CHAT_MODEL, model_provider='ollama')


def llm_node(state):
    response = llm.invoke(state['messages'])
    return {'messages': state['messages'] + [response]}


def router(state):
    last_message = state['messages'][-1]
    return 'tools' if getattr(last_message, 'tool_calls', None) else 'end'



tool_node = ToolNode([get_current_weather, suggest_activity])


def tools_node(state):
    result = tool_node.invoke(state)

    return {
        'messages': state['messages'] + result['messages']
    }



builder = StateGraph(ChatState)
builder.add_node('llm', llm_node)
builder.add_node('tools', tools_node)
builder.add_edge(START, 'llm')
builder.add_edge('tools', 'llm')
builder.add_conditional_edges('llm', router, {'tools': 'tools', 'end': END})

graph = builder.compile()


if __name__ == '__main__':
    state = {'messages': []}

    print('Type an instruction or "quit".\n')

    while True:
        user_message = input('> ')

        if user_message.lower() == 'quit':
            break
        if user_message == '':
            user_message = "What's the weather like in London, and what activity should I do based on that?"
            print("Using default query:", user_message)

        state['messages'].append({'role': 'user', 'content': user_message})

        state = graph.invoke(state)

        print(state['messages'][-1].content, '\n')
