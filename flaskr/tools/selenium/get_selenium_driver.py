# download driver from https://googlechromelabs.github.io/chrome-for-testing/
import socket
import os
# import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# you need first to run the chrome driver in cmd (.\chromedriver.exe --port=5000)
def connect_to_driver():
    if not check_port_is_open("localhost", 5000):
        # current_folder = os.path.dirname(os.path.abspath(__file__))
        # find path installed chrome driver
        # chromedriver_path = os.path.join(current_folder, "chromedriver.exe")
        # chrome_install = ChromeDriverManager().install()
        # folder = os.path.dirname(chrome_install)
        # chromedriver_path = os.path.join(folder, "chromedriver.exe")
        raise Exception("run the chrome driver in cmd (.\chromedriver.exe --port=5000)")
    options = Options()
    options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(options=options)
    url = "http://127.0.0.1:5000"  # driver.command_executor._url
    options.add_experimental_option("detach", True)
    driver = webdriver.Remote(command_executor=url, options=options)
    session_id = ""
    # 4. And you are connected to your driver again.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    FILE_NAME = dir_path + "\\session_id.txt"
    with open(FILE_NAME, "r") as f:
        session_id = f.read()
    new_session_id = driver.session_id
    driver.session_id = session_id
    try:
        # driver.get("https://www.neuralnine.com/")
        url = driver.current_url
        driver.session_id = new_session_id
        # this prevents the dummy browser
        driver.close()
        driver.session_id = session_id
    except:
        driver.session_id = new_session_id
        with open(FILE_NAME, "w") as f:
            f.write(driver.session_id)
    url = driver.current_url
    print(driver.session_id)
    return driver


def check_port_is_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, int(port)))
        return True
    except:  # pylint: disable=bare-except
        return False
    finally:
        sock.close()

def get_all_sesions(driver):
    import requests
    # URL to get all sessions from Chromedriver
    url = "http://localhost:5000/sessions"
    # Send request to Chromedriver
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        sessions = response.json().get("value", [])
        return [session["id"] for session in sessions]
    else:
        print(f"Failed to get sessions: {response.status_code}")


if __name__ == "__main__":
    driver = connect_to_driver()
    print("all sessions:",get_all_sesions(driver))
    driver.get("https://google.com/")
