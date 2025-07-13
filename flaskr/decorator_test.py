from functools import wraps


def my_decorator(*args, **kwargs):
    decArgs = args
    decOptKwargs = kwargs

    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print("Calling decorated function")
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
                print(
                    "{0} = {1}".format(key, value)
                )  # not printing defalt fun optional but this is working
            # call back to the function or don't if condition fail
            return f(*args, **kwargs)

        return wrapper

    return actual_decorator


@my_decorator("mast", dec_opt="optional")
def example(inn: int, fun_opt=" fun optional"):
    """Docstring"""
    print("Called example function with ars: " + str(inn) + "," + fun_opt)


example(5, fun_opt=" fun optional call")
