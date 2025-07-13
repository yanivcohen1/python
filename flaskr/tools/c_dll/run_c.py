import ctypes
import json
import os
import base64

def test_str():

    # Example input JSON
    input_json = json.dumps({"key": "value"})

    # Call the C function
    output_json_bin = lib.process_json(input_json.encode('utf-8'))
    output_json = output_json_bin.decode('utf-8')

    # Print the output JSON
    print("py print:", output_json)

def test_file():
    file_path = r"C:\Users\yaniv\OneDrive\python-flask\flaskr\tools\flask_sql_alchemy\upload_download\hero.jpg"
    # Open the file in binary mode and send it using a POST request
    with open(file_path, 'rb') as file:
        files = file.read()
    file_64_bin = base64.b64encode(files)# .decode()

    # Call the C function
    output_bin = lib.process_file(file_64_bin)
    # output_json = output_json_bin.decode('utf-8')

    file_dec_bin = base64.b64decode(output_bin)
    file_down_path = r"C:\Users\yaniv\OneDrive\python-flask\flaskr\tools\flask_sql_alchemy\upload_download\hero2.jpg"
    with open(file_down_path, 'wb') as file:
        file.write(file_dec_bin)

currentDir = os.path.join(os.path.dirname(__file__))
# Load the shared dll library win
lib = ctypes.CDLL(currentDir + '/jsonprocess.dll')
# Load the shared so library linux
# lib_linux = ctypes.CDLL(currentDir + '/ibjsonprocess.so')

# Define the argument and return types of the C function
lib.process_json.argtypes = [ctypes.c_char_p] # input c char pointer
lib.process_json.restype = ctypes.c_char_p # output c char pointer

lib.process_file.argtypes = [ctypes.c_char_p]
lib.process_file.restype = ctypes.c_char_p

if __name__ == '__main__':
    test_str()
    test_file()
