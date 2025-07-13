# 1. Install dependencies
#    pip install -U langgraph langchain-openai langchain-ollama semantic-router
import json
from langchain.tools import Tool
from langchain_ollama.llms import OllamaLLM
# from langchain_community.chat_models import ChatOllama
from langchain_ollama.chat_models import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

# 2. Define your “tools” as Python callables:
def calculator(expr: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Calculation Error: {e}, expr: {expr}"

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
        description="Useful for math operations. Input should be a valid Python math expression without variables."
    ),
    Tool(
        name="Weather",
        func=weather_tool,
        description="Provides current weather info. Input should be like 'Paris in Celsius' or 'New York in Fahrenheit'"
    ),
    Tool(
        name="Web Search",
        func=search_tool.run,
        description="Useful for when you need to answer questions about current events and general knowledge. Input should be a search query.",
    )
]

# 3. Spin up your Ollama‑powered LLM
llm = ChatOllama(
    model="qwen3:1.7b", # qwen3:4 bmistral deepseek-coder-v2:16b gemma3:4b
    # api_key="ollama",
    # base_url="http://localhost:11434/v1",
)

# 4. Bind the tools and build a ReAct agent graph
llm_with_tools = llm.bind_tools(tools)
agent = create_react_agent(llm_with_tools, tools)

query = "first step find What is the weather in Cairo, second step multiple the tempurture from first step in 10?"
# 5. Invoke the agent
for chunk in agent.stream({
    "messages": [("user", query),("system", "Please answer in a step-by-step manner. use only the tools you have,\
                                  all calculation will be only with Calculator tool\
                                  all weather information will be only with Weather tool")],
}, stream_mode="messages"):
    if chunk[0].content:
        print(chunk[1]["langgraph_node"],':', chunk[0].name, "-", chunk[0].content, end="\n")

# 6. Print out the step‑by‑step reasoning and final answer
#for msg in response["messages"]:
#    print(msg.content)
