import ollama
import json

# Define your Python tools

def get_time() -> str:
    """Returns the current server date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def uppercase(text: str) -> str:
    """Converts input text to uppercase."""
    return text.upper()


def reverse(text: str) -> str:
    """Reverses the input text."""
    return text[::-1]

# Map from tool name to function object
TOOLS = {
    'get_time': get_time,
    'uppercase': uppercase,
    'reverse': reverse,
}

# Ask user for permission before running a tool

def ask_permission(name: str, args: dict) -> bool:
    print(f"Agent requests to run: {name} with arguments: {args}")
    resp = input("Do you allow this? (y/n): ")
    return resp.strip().lower() == 'y'

# Execute a single tool call

def execute_tool_call(tool_call) -> str:
    name = tool_call.function.name
    args = tool_call.function.arguments or {}
    func = TOOLS.get(name)
    if func is None:
        return f"Error: Unknown tool '{name}'"
    if not ask_permission(name, args):
        return f"Permission denied for tool: {name}"
    try:
        # Call with keyword args if any, else no args
        return func(**args)
    except Exception as e:
        return f"Error running {name}: {e}"

# Main agent loop
if __name__ == '__main__':
    # Start conversation history
    history = [
        {'role': 'system', 'content': 'if "role: tool" and "name: tool_name", then use this "content: content" as tool_name answer no need to rerun the tool'},
        {'role': 'user', 'content': input('You: ')} # get the time and reverse it
    ]
    i = 0
    while True:
        i = i + 1
        print(f"\n--- Iteration {i} ---")
        # Call the model with available Python tools
        response = ollama.chat(
            'qwen3:1.7b', # 'llama3.1:8b'  # or your preferred model
            messages=history,
            tools=list(TOOLS.values())
        )

        # Otherwise handle tool calls
        for tool_call in response.message.tool_calls or []: # pylint: disable=E1101
            # Append the model's tool call to history
            history.append({'role': 'assistant', 'tool_call': tool_call})
            # Execute and append function result
            result = execute_tool_call(tool_call)
            history.append({
                'role': 'tool',
                'name': tool_call.function.name,
                'content': result
            })
            break
        # Loop again to let the model process the function results

        # If model returned a content message, it's the final answer
        if not response.message.get('tool_calls') and response.message.content: # pylint: disable=E1101
            print('Final Answer:', response.message.content) # pylint: disable=E1101
            break
