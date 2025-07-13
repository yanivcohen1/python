import inspect
from typing import get_type_hints
import ref as module
# import importlib
# import reflaction

# for dynamic import of a module
# module = importlib.import_module("your_module")

# Inspect module-level variables (with type hints if available)
print("------------Module variables--------------")
var_hints = get_type_hints(module)
for name, value in module.__dict__.items():
    if not name.startswith("__") and not inspect.isroutine(value) and not inspect.isclass(value):
        type_hint = var_hints.get(name, type(value).__name__)
        print(f"  {name} ({type_hint}) = {repr(value)}")

print("\n------------Module functions--------------")
var_hints = get_type_hints(module)
for name, value in module.__dict__.items():
    if not name.startswith("__") and inspect.isroutine(value) and not inspect.isclass(value):
        type_hint = var_hints.get(name, type(value).__name__)
        func = value
        print(f"Function name: {func.__name__}")
        print("Parameters:")
        for param in inspect.signature(func).parameters.values():
            param_type = param.annotation.__name__ if param.annotation is not param.empty else ""
            param_default = "= " + str(param.default) if param.default is not param.empty else ""
            print(f"  {param.name}: ({param_type}) {param_default}")
        print("Return type:", inspect.signature(func).return_annotation.__name__ or "None")

        print("Docstring:", func.__doc__)
        print("\nSource code:", inspect.getsource(func))
        print("\nLine number:", inspect.getsourcelines(func)[1])
        print("\nFile name:", inspect.getfile(func))
        print("\nModule name:", func.__module__)

print("\n-----------Module info---------------")
# module = importlib.import_module("your_module")
print("\nModule file:", module.__file__)
print("\nModule name:", module.__name__)
print("\nModule package:", module.__package__)
print("\nModule cached:", module.__cached__)
print("\nModule loader:", module.__loader__)
print("\nModule dict:", module.__dict__)
