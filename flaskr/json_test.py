import json
# python dictionary
dictionary = {} # empty dictionary
dictionary = {"age":30, "last":{"name": "cohen"}, "first":[{"name":"yaniv"}, {"age":30}]}

# python parse dictionary to JSON staring
JsonString = json.dumps(dictionary)
print(JsonString) # print '{"age":30, "last":{"name": "cohen"}, "first":[{"name":"yaniv"}, {"age":30}]}'

# python parse JsonString to dictionary:
dictionary = json.loads(JsonString)

# the result is a Python dictionary:
print(dictionary["first"][0]["name"]) # print yaniv
print(dictionary["last"]["name"]) # print cohen

# javascript parse JSON string to JSON
# Json = {} // empty json
# json = JSON.parse(JsonString)
# javascript pars JSON to JSON string to send it
# JsonString = JSON.stringify(json)