import requests
import json
import socket

headers_json = {"Content-Type": "application/json; charset=utf-8"}

def get(URL_WithParams, headers):
    response = requests.get(URL_WithParams, headers=headers)
    # print("get:", response.text[:7])
    return response.text

def post_data(URL_WithParams, postdata, headers):
    # postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
    resp = requests.post(URL_WithParams, data=postdata, headers=headers) # post body params
    # print('post:', resp.text[:7])
    return resp.text# return as text

def post_json(URL_WithParams, json, headers):
    # postdata = {"firstname": "John", "lastname": "Doe"} # params from dict
    resp = requests.post(URL_WithParams, json=json, headers=headers) # post body params
    # print('post:', resp.text[:7])
    return resp.json()# return as json

def send_rcv_cookies_and_download_file():
    session = requests.Session()
    url = 'http://google.com/favicon.ico'
    cookies = {'cookies_are': 'working'}
    myJson = {'somekey': 'somevalue'}
    headers={"Content-Type":"json"}
    response = session.post(url, allow_redirects=True, headers=headers, cookies=cookies, json = myJson)
    open('google.ico', 'wb').write(response.content) # download file
    session.cookies.set("cookie_name", "cookie_value")
    session.cookies.set("cookie_name2", "cookie_value2")
    session.cookies.get("cookie_name")
    print("print the cookies", session.cookies.get_dict())
    print("print the headers", response.headers)
    print("json of response", response.json)
    print("text of response", response.text)

def get_socket():
    # get or post with socket
    # get http://ip-api.com/json/24.48.0.1
    HOST = "ip-api.com"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, 80))
    # get for url about.html
    PATH = "json/24.48.0.1"
    content_type="application/json; charset=utf-8"

    header_bytes = f"""\r
GET /{PATH} HTTP/1.1\r
Host:{HOST}\r
Connection: close\r
\r\n"""
    # header_bytes = "GET /"+PATH+" HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n"
    # sock.send(b"GET /about.html HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n")
    # ...
    sock.send(header_bytes.encode())
    response = sock.recv(4096).decode()

    print(response)
    val = response.split('\r\n\r\n',1)[1]
    # json1 = json.loads(val)
    #print(json1)
    sock.close()

def post_socket():
    host = "httpbin.org"
    port = 80

    headers = """\r
    POST /{route} HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""

    postData = {
                "Id": 78912,
                "Customer": "Jason Sweet",
                "Quantity": 1,
                "Price": 18.00
                }
    body = json.dumps(postData)# 'userName=Ganesh&password=pass'
    body_bytes = body.encode('ascii')
    header_bytes = headers.format(
        # content_type="application/x-www-form-urlencoded",
        content_type="application/json; charset=utf-8",
        content_length=len(body_bytes),
        host=str(host) + ":" + str(port),
        route = "/post"
    ).encode('iso-8859-1')

    payload = header_bytes + body_bytes

    # ...
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 80))
    sock.sendall(payload)
    response = sock.recv(4096).decode()
    print(response)

if __name__ == '__main__':
    # get
    print("\n--------- from get --------------")
    url = "http://ip-api.com/json/24.48.0.1"
    headers_json = {"Content-Type": "application/json; charset=utf-8"}
    resp = get(url, headers_json)
    print(resp)
    # post
    print("\n--------- return post data --------------")
    postData = {
                "Id": 78912,
                "Customer": "Jason Sweet",
                "Quantity": 1,
                "Price": 18.00
                }
    url = "https://httpbin.org/post"
    resp = post_data(url, json.dumps(postData), {})
    print(resp)

    print("\n--------- return post json --------------")
    resp = post_json(url, postData, {})
    # json1 = json.loads(resp["json"])
    print(resp)

    print("\n---------get socket --------------")
    get_socket()

    print("\n---------post socket --------------")
    post_socket() # https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST#example
