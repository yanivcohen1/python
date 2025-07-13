import os
import re
import requests
import base64

host = 'http://127.0.0.1:5000'
file_id = None
# First, upload a file
def upload():
    url = host + '/upload'
    file_path = r"C:\Users\yaniv\OneDrive\python-flask\flaskr\tools\flask_sql_alchemy\upload_download\hero.jpg"

    # Open the file in binary mode and send it using a POST request
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)

    # Print the response
    if response.status_code == 200:
        file_id = response.json().get("file_id")
        print("upload file id:", file_id)
    else:
        print("Error uploading file")
    return file_id


# Next, download the file
def download():
    url = host + '/download/' + str(file_id)
    file_path = r'C:\Users\yaniv\OneDrive\python-flask\flaskr\tools\flask_sql_alchemy\upload_download/'

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print("Error downloading file")
        return False
    content_disposition = response.headers.get("Content-Disposition")
    filename = re.findall('filename="?([^"]+)"?', content_disposition)
    name, extension = os.path.splitext(filename[0])
    file_full_download_path = file_path + name + "-download" + extension
    print("downloaded file path:", file_full_download_path)
    # Save the content of the response to a file
    with open(file_full_download_path, 'wb') as file:
        file.write(response.content)
    return True


if __name__ == '__main__':
    # file_id = upload()
    file_id = 1
    download()
