import pickle
import json

# Create a variable
myvar = [{'This': 'is', 'Example': 1}, 'of',
          'serialisation', ['using', 'pickle']]

print("To serialized msg:", myvar)
# Use dumps() to make it serialized
serialized_bytes = pickle.dumps(myvar)
print("serialized msg:", serialized_bytes)

unSerialized = pickle.loads(serialized_bytes)
print("UnSerialized msg:", unSerialized)

# -------------------------------------------------------
# serialized to text by json
myvar = [{'This': 'is', 'Example': 1}, 'of',
          'serialisation', ['using', 'pickle']]

print("\nJson obj to json str:", myvar)
# Use dumps() to make it serialized
json_str = json.dumps(myvar)
print("json str msg:", json_str)

json_obj = json.loads(json_str)
print("Form json str to json obj:", json_obj)
