# How to see the list of methods attached to an objects?
name='Michaela'
print(dir(name)) # gives the list of methods attached to the variable "name"
import os
print(str(os.path))
print(help(str)) # gives explanations about all the methods of the object "str" (string)
print(help(str.lower)) # gives explanations about the method "lower"
# print all evleble models
help('modules')

print("-------------str------------------")
str(os.path)
print("-------------fun help------------------")
help(os.path)
print("-------------module help------------------")
help(os)
# help(module.funName)
# help(class.funName)
# obj = class()
# str(obj)

# ------- fileNmae.py -h or --help
import argparse
parser = argparse. ArgumentParser (description="Meow like a cat")
parser.add_argument("-n", help="number of times to meow")
args = parser.parse_args()
for _ in range(int(args.n)):
    print("meow")
