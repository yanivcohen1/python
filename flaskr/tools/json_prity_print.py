import requests
import json

# Define the URL where the JSON is located
url = 'https://api.github.com/users/mralexgray/repos'

# Make a GET request to the URL
response = requests.get(url, timeout=10)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response content
    json_data = response.json()

    # Print or process the JSON data
    print(json.dumps(json_data, indent=4))
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
