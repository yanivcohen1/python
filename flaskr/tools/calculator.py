import math


def calculator(expr: str) -> str:
    """
    Safely evaluate a mathematical expression string that may include
    functions from the math module (e.g., sin, cos, sqrt, pi, etc.).

    Args:
        expr (str): The math expression to evaluate.

    Returns:
        float: The result of the evaluated expression.
    """
    # Allowed names: all functions/constants from math
    allowed_names = {
        name: getattr(math, name) for name in dir(math) if not name.startswith("__")
    }

    # Add common built-in constants
    allowed_names.update({"pi": math.pi, "e": math.e})

    try:
        return str(eval(expr, {"__builtins__": {}}, allowed_names))
    except Exception as e:
        return f"Calculation Error: {e}, expr: {expr}"


# Example usage
print(calculator("sin(pi / 2) + sqrt(16)"))  # 5.0
print(calculator("log(e) * acos(0)"))  # 1.0
print(calculator("2 ** 8 + tan(pi / 4)"))  # 257.0
print(calculator("invalid_function(2)"))  # Calculation Error: name 'invalid_function' is not defined
print(calculator("10 / 0"))  # Calculation Error: division by zero, expr: 10 / 0

print(calculator("tan(acos(8/14)/2)*8"))
