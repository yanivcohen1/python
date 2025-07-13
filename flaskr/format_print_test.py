import math

hith = 5_000 # same as 5000
radius = 10.543
volume = int(math.pi * radius * radius * hith)
# print radius in 2 dig after the point
print(f'The chlinder hith: {hith} and the radius: {radius:.2} = \
so the volume is:{int(math.pi * radius * radius * hith)} \n The End resoult need to be {volume}')

class class1():
    name = 'yaniv cohen'

    def __init__(self, name) -> None:
        self.name = name

    def say_hi(self):
        print(self.name + " takes care of you!")

c1 = class1('yanic')
print(f'\nThe class1 funcions and variables: {dir(class1)}')
print(f'\nThe c1 funcions and variables: {dir(c1)}')
print(f'\nThe c1 type: {type(c1)}')
print(f'is c1 is type of class1: {isinstance(c1, class1)}')
print(f'\n Th\\e c\'1 typ\\\'e: {type(c1)}') # Th\e c'1 typ\'e:

print("can\"t") # can"t
print("can\\\"t") # can\"t
print("can\\t") # can\t
