import requests

host = 'http://127.0.0.1:5000'

# no need to login to access this route
url = host+"/api/find_books_by_author_name?author_name=F. Scott Fitzgerald"
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
login_response = requests.post(login_url, json=login_data)
access_token = login_response.json().get("access_token")
# Use the access token to access the protected route
headers = {
    "Authorization": f"Bearer {access_token}"
}
print('access_token:', access_token)

url = host+"/protected"
response = requests.get(url, headers=headers)
print('protected:', response.json())

url = host+"/get_user_id"
response = requests.get(url, headers=headers)
print('get_user_id:', response.text)
