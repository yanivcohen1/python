from scapy.layers.http import http_request

# Define the IP address and port of the server you want to connect to
ip = "google.com"
port = 80

# Define the HTTP GET request
# http_request = "GET / HTTP/1.1\r\nHost: " + ip + "\r\n\r\n"

# Send the HTTP request and receive the response
response = http_request(host=ip, port=port, path="/",Method="GET", Unknown_Headers={"User-Agent": "Mozilla/5.0"})

# Print the response
print(response.show())