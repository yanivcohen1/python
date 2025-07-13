# args type Arry, kwargs type dictionery
# args & kwargs Are optional
def func(required_arg, *args, **kwargs):
    # required_arg is a positional-only parameter.
    print(required_arg)

    # args is a tuple of positional arguments,
    # because the parameter name has * prepended.
    if args: # If args is not empty.
        print(args)

    # kwargs is a dictionary of keyword arguments,
    # because the parameter name has ** prepended.
    if kwargs: # If kwargs is not empty.
        print(kwargs)

# func()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: func() takes at least 1 argument (0 given)

func("required argument")
#required argument

func("required argument", 1, 2, '3')
# required argument
# (1, 2, '3')

func("required argument", 1, 2, '3', keyword1=4, keyword2="foo")
# required argument
# (1, 2, '3')
# {'keyword2': 'foo', 'keyword1': 4}

def my_function(**kid):
  print("His last name is: '" +  kid["last"] + "', and number: " + str(kid["number"]))

json1 = {'fname': 'Tobias', 'number': 3} # dictionery
my_function(**json1, last='last1')
