import requests
import json

headers_json = {"Content-Type": "application/json; charset=utf-8"}

def get(URL_WithParams, headers):
    response = requests.get(URL_WithParams, headers=headers)
    # print("get:", response.text[:7])
    return response

def post(URL_WithParams, postdata, headers):
    # postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
    resp = requests.post(URL_WithParams, data=postdata, headers=headers) # post body params
    # print('post:', resp.text[:7])
    return resp

def post_json(URL_WithParams, json, headers):
    # postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
    resp = requests.post(URL_WithParams, json=json, headers=headers) # post body params
    # print('post:', resp.text[:7])
    return resp

def send_rcv_cookies_and_download_file():
    session = requests.Session()
    url = 'http://google.com/favicon.ico'
    cookies = {'cookies_are': 'working'}
    myJson = {'somekey': 'somevalue'}
    headers={"Content-Type":"json"}
    response = session.post(url, allow_redirects=True, headers=headers, cookies=cookies, json = myJson)
    open('google.ico', 'wb').write(response.content) # download file
    print("print the cookies", session.cookies.get_dict())
    print("print the headers", response.headers)
    print("json of response", response.json)
    print("text of response", response.text)

if __name__ == '__main__':
    # get
    url = "http://ip-api.com/json/24.48.0.1"
    headers_json = {"Content-Type": "application/json; charset=utf-8"}
    resp = get(url, "")
    print("GET response as text: \n",resp.text)
    # post
    postData = {
                "Id": 78912,
                "Customer": "Jason Sweet",
                "Quantity": 1,
                "Price": 18.00
                }
    url = "https://httpbin.org/post"
    resp = post_json(url, postData, "")
    # json1 = json.loads(resp["json"])
    print("\n POST Json and response cast to json: \n",resp.json())
    resp = post(url, json.dumps(postData), "")
    print("\n POST text and response ad text: \n",resp.text)
