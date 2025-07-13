from typing import Final # in python 3.8 >=

a: Final = 1.2
b: float = 2
c = (1,2,3) # tuple is read only
# Executes fine, but mypy will report an error if you run mypy on this:
# a = 2 # editor error
c[0] = 2 # runtime error - tuple is read only
print(a)
