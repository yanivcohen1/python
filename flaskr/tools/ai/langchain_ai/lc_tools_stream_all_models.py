# 1. Install dependencies
#    pip install -U langgraph langchain-openai langchain-ollama semantic-router
import json
from langchain.tools import Tool
from langchain_ollama.llms import OllamaLLM
# from langchain_community.chat_models import ChatOllama
from langchain_ollama.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper

# 2. Define your “tools” as Python callables:
def calculator(expr: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Calculation Error: {e}, expr: {expr}"

def weather_tool(city: str, format: str = "Celsius") -> str:
    fake_data = {
        "new york": "15°C, cloudy",
        "london": "10°C, rainy",
        "cairo": "28C, sunny",
        "paris": "12°C",# , windy
        "tokyo": "20°C, clear",
    }
    return fake_data.get(city.lower(), "Weather data not available.")

def weather_tool_input_parser(json_str: str) -> str:
    try:
        data = json.loads(json_str)
        city = data.get("city")
        format = data.get("format", "Celsius")
        return weather_tool(city, format)
    except Exception as e:
        return f"Invalid input format. Please provide JSON like {{'city': 'Paris', 'format': 'Celsius'}}. Error: {e}, json is {json_str}"

# Initialize DuckDuckGo search tool
search_tool = DuckDuckGoSearchRun()
# Initialize Wikipedia API
wiki = WikipediaAPIWrapper()

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math operations. Input should be a valid Python math expression."
    ),
    Tool(
        name="Weather",
        func=weather_tool_input_parser,
        description='''Gives current weather for a city.
                        Input should be a JSON string with 'city' and optional 'format' (Celsius).
                        for example: {"city": "london","format": "Celsius"}'''
    ),
    Tool(
        name="Web Search",
        func=search_tool.run,
        description="Useful for when you need to answer questions about current events. Input should be a search query.",
    ),
    Tool(
        name="Wikipedia Search",
        func=wiki.run,
        description="Useful for when you need to answer questions from Wikipedia for general knowledge. Input should be a search query.",
    )
]

# 3. Spin up your Ollama‑powered LLM
llm = OllamaLLM(
    model="deepseek-coder-v2:16b", # mistral  gemma3:4b
    # api_key="ollama",
    # base_url="http://localhost:11434/v1",
)

# https://www.promptingguide.ai/techniques/react
# both reasoning traces and task-specific actions
template_reAct = """you provided with the Previous conversation: {chat_history}
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}] or from {chat_history}, otherwise "I don't know"
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
# agent_scratchpad helps by inserting the history of tool calls, observations, and thoughts back into the prompt.
# Action: the action to take, should be one of [{tool_names}] if possible, otherwise "I don't know"

prompt = PromptTemplate.from_template(template_reAct)

# 4. Bind the tools and build a ReAct agent graph
# llm_with_tools = llm.bind_tools(tools)
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    # verbose=True, # Set to True to see the agent's thought process
    # handle_parsing_errors=True # Helps if the LLM output isn't perfectly formatted
)
# 5. Invoke the agent
chat_history = ""
while True:
    print("\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    while True:
        if question == "q":
            break
        if question == "":
            question = "What is the weather in Paris in Celsius and convert it to Fahrenheit, and what is a Pencil used for, and who is the current USA presedent?"
            print("question is: ", question, "\n")
        ans = ''
        try:
            for chank in agent_executor.stream({"input": question, "chat_history": chat_history}):
                if 'messages' in chank:
                    if 'Agent stopped due to iteration limit or time limit' in chank['messages'][0].content:
                        continue
                    ans += chank['messages'][0].content
                    print(chank['messages'][0].content, end="\n")
                # elif 'output' in chank:
                #     print(chank['output'], end="\n")
            break
        except Exception as e:
            continue
    chat_history += question
    # break
