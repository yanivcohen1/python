from typing import Any

last_names = "reflaction"
arry = [1, 2]

def add(a: Any, b: int) -> int:
    """Add two numbers.
    Args:
        a (int): The first number.
        b (int): The second number.
    Returns:
        int: The sum of the two numbers.
    """
    return a + b

def greet(name: str, age: int = 10) -> str:
    """Greet a person with their name and age.
    Args:
        name (str): The name of the person.
        age (int): The age of the person.
    Returns:
        str: A greeting message.
    """
    # last_name = "reflaction"
    return f"Hello {name}, you are {age}."
