import json
import requests

host = 'http://127.0.0.1:5000'

# no need to login to access this route
url = host+ '/books'#"/find_books_by_author_name?author_name=F. Scott Fitzgerald"
headers = { 'Custom-Header': 'CustomValueSend' }
response = requests.get(url, headers=headers)
print('find_books_by_author_name:', response.json())
# Access a specific header
custom_header = response.headers.get('Custom-Header')
print(f'Custom-Header: {custom_header}')

# First, login to get the JWT access token
login_url = host+"/login"
login_data = {
    "username": "yaniv",
    "password": "yaniv_P"
}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
login_response = requests.post(login_url, data=f"username=yaniv&password=yaniv_P", headers=headers)
access_token = json.loads(login_response.text).get("access_token")
# Use the access token to access the protected route
headers = {
    "Authorization": f"Bearer {access_token}"
}
print('access_token:', access_token)

# url = host+"/protected"
# response = requests.get(url, headers=headers)
# print('protected:', response.json())

url = host+"/get_user_name"
response = requests.get(url, headers=headers)
print('get_user_name:', response.text)
