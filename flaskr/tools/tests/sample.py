import random
import time
import requests

def my_str(strs):
    return ""

def random_sum():
    a = random.randint(1, 10)
    b = random.randint(1,7)
    return a + b if not my_str("test") else my_str("mock")

def silly():
    params = {
    "timestamp": time.time(),
    "number": random.randint(1, 6)
    }
    response = requests.get("https://httpbin.org/get", params)
    if response.status_code == 200:
        return response.json()['args']

if __name__ == '__main__':
    print(random_sum()) # 5
    print(silly()) # {'number': '6', 'timestamp': '1733916375.8652258'}
