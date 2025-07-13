A = 1
B = 2

def my_fun(a):
    global A
    A = a

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def set_job(self, job):
        self.job = job

p = Person("Mike", 30)
p.set_job("Programmer")

print('A' in dir())
print('name' in dir(p))
print('my_fun' in dir())
print('is var is fun:', callable(my_fun))

print(dir()) # all variables

my_fun(5)
print(vars()['A']) # get values from var
print(vars(p)['name']) # get name from obj p from class Person
print(vars()) # all variables and there values
