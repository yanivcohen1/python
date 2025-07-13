import logging
import json
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.tools import Tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

# 1) Silence httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# 2) Simple token‑printer callback
class TokenPrinter(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)

cb_manager = CallbackManager([TokenPrinter()])

# 3) Define tools
def calculator(expr: str) -> str:
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}, expr: {expr}"

def weather_tool(raw_input: str) -> str:
    # Basic parsing from raw input like "Paris in Celsius" or "Tokyo in Fahrenheit"
    parts = raw_input.strip().split(" in ")
    if len(parts) == 2:
        city, format = parts[0], parts[1].capitalize()
    else:
        city, format = raw_input.strip(), "Celsius"  # Default to Celsius
    fake_data = {
        "new york": "15°C, cloudy",
        "london": "10°C, rainy",
        "cairo": "28"
    }
    return fake_data.get(city.lower(), "Weather data not available.")

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math operations. Input should be a valid Python math expression."
    ),
    Tool(
        name="Weather",
        func=weather_tool,
        description="Provides current weather info. Input should be like 'Paris in Celsius' or 'New York in Fahrenheit'"
    )
]


# 4) Ollama LLM with streaming + our token‑printer
llm = ChatOllama(
    model="qwen3:1.7b", # qwen3:4b mistral
    # api_key="ollama",
    # base_url="http://localhost:11434/v1",
    # streaming=True,
    # callback_manager=cb_manager,
)

# 5) Build the ReAct agent
agent = create_react_agent(llm.bind_tools(tools), tools)

query = "What is the weather in Cairo in Celsius and calculate the convertion to Fahrenheit?"
# 6) Invoke with a system prompt that *forces* ReAct formatting
print("=== Agent reasoning trace ===")
# Replace agent.invoke(...) with agent.stream(...)
for chunk in agent.stream(
    {
        "messages": [
            ("system",
              "You are a ReAct agent. Always think step-by-step and emit lines prefixed with:\n"
              "  Thought: …\n"
              "  Action: …\n"
              "  Action Input: …\n"
              "  Observation: …\n"
              "Then at the end print:\n"
              "  Final Answer: …"
            ),
            ("user", query)
        ]
    },
    stream_mode="messages"   # only get the LLM’s token stream
):
    if chunk[0].content:
        if chunk[1]["langgraph_node"] == "tools":
            print(chunk[1]["langgraph_node"], ':', chunk[0].name, "-", chunk[0].content, end="\n")
        else:
            print("Agent:", chunk[0].content, end="\n")
