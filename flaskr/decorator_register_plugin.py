from functools import wraps
import random
from typing import List, Dict

FUNCTIONS = dict()
ARGUMENTS: List[Dict] = []


def register(*args, **kwargs):
    decArgs = args
    decOptKwargs = kwargs
    ARGUMENTS.append(kwargs)

    def actual_decorator(func):
        FUNCTIONS[func.__name__] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Calling decorated function')
            print("Decorator arguments: ")
            for arg in decArgs:
                print(arg)
            print("Decorator kwargs optional arguments: ")
            for key, value in decOptKwargs.items():
                print("{0} = {1}".format(key, value))

            print("function arguments: ")
            for arg in args:
                print(arg)
            print("function kwargs optional arguments: ")
            for key, value in kwargs.items():
                # not printing defalt fun optional but this is working
                print("{0} = {1}".format(key, value))
            # call back to the function or don't if condition fail
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator


@register(name="reg1")
def say_hello(name):
    return f"Hello {name}"


@register(name="reg2", family="reg3")
def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"


def randomly_greet(name):
    greeter, greeter_func = random.choice(list(FUNCTIONS.items()))
    print(f"Using {greeter!r}")
    return greeter_func(name)


for keys, value in FUNCTIONS.items():
    print(keys + " : ", value)

print("-----------------")
for args in ARGUMENTS:
    for keys, value in args.items():
        print(keys + " : ", value)
    print("-------")

print("-----------------")
print(randomly_greet("Alice"))
