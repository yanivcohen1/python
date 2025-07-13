class Example:
    staticVariable = 5 # Access through class

    def read_only_var(self):
        pi = 3.14
        return pi

print(Example.staticVariable) # prints 5

# Access through an instance
instance = Example()
print(instance.staticVariable) # still 5

# Change within an instance
instance.staticVariable = 6
print(instance.staticVariable) # 6
print(Example.staticVariable) # 5

# Change through
Example.staticVariable = 7
print(instance.staticVariable) # still 6
print(Example.staticVariable) # now 7

# read only var
print(instance.read_only_var()) # pi