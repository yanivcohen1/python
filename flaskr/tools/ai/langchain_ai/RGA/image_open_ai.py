import base64
import os
import httpx
from langchain_core.messages import HumanMessage
# Import the updated Ollama model from the new package
from langchain_ollama.llms import OllamaLLM
from langchain_openai import ChatOpenAI
from typing import Literal
from langchain_core.tools import tool

current_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.abspath(current_path + "/../content/images/")

model = ChatOpenAI(
        api_key="your_api_key_here",  # Replace with your actual API key
        temperature=0.8,
        model="gemma3:4b",  # or "gpt-3.5-turbo"
        base_url="http://localhost:11434/v1"
        # stream_usage=True,
        # callback_manager=callback_manager
)

@tool
def weather_tool(weather: Literal["sunny", "cloudy", "rainy"]) -> None:
    """Describe the weather"""
    pass


model_with_tools = model.bind_tools([weather_tool])

def convert_to_base64(image_path: str) -> str:
    """
    Opens an image file and converts it to a base64-encoded string.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
pic_name = 'cow.jpg'  # "cow.png"
image_data = convert_to_base64(f"{images_path}/{pic_name}")
image_data_url = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
message_embed = HumanMessage(
    content=[
        {"type": "text", "text": "describe the weather in this image"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}, # image_data
        },
    ],
)

message_url = HumanMessage(
    content=[
        {"type": "text", "text": "describe the weather in this image"},
        {"type": "image_url", "image_url": {"url": image_url}},
    ],
)

# response = model_with_tools.invoke([message_embed])
response = model.invoke([message_embed])
print(response.content)

# print("calling tool: weather_tool")
# print(response.tool_calls)
# [{'name': 'weather_tool', 'args': {'weather': 'sunny'}, 'id': 'call_BSX4oq4SKnLlp2WlzDhToHBr'}]
