# PythonDecorators/decorator_with_arguments.py
class decorator_with_arguments(object):

    def __init__(self, *args, **kwargs):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        print("Inside __init__()")
        self.decArgs = args
        self.decOptKwargs = kwargs

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print("Inside __call__()")
        def wrapped_f(*args, **kwargs):
            print("Inside wrapped_f()")
            print("Decorator arguments: ")
            for arg in self.decArgs:
                print (arg)
            print("Decorator kwargs optional arguments: ")
            for key, value in self.decOptKwargs.items():
                print("{0} = {1}".format(key, value))
            f(*args, **kwargs) # call back to the function or don't if condition fail
            print("After f(*args)")
        return wrapped_f

# PythonDecorators/decorator_with_arguments.py
class decorator_without_arguments2(object):

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        print("Inside __call__2()")
        def wrapped_f(*args, **kwargs):
            print("Inside wrapped_f2()")
            # print("Decorator arguments:", self.arg1, self.arg2, self.arg3)
            f(*args, **kwargs) # call back to the function or don't if condition fail
            print("After f(*args)2")
        return wrapped_f

@decorator_with_arguments("hello", "world", dec_opt="dec-optional")
@decorator_without_arguments2()
def sayHello(a1, a2, a3, a4, fun_opt="fun-optional"):
    print('sayHello arguments:', a1, a2, a3, a4, fun_opt)

print("After decoration")

print("Preparing to call sayHello()")
sayHello("say", "hello", "argument", "list", fun_opt="fun-optional-call")
print("after first sayHello() call")
print()
sayHello("a", "different", "set of", "arguments")
print("after second sayHello() call")