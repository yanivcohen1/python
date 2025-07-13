import requests
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

# --allow-cors -Selenium server should allow web browser connections from any host
# --session-timeout 999999 in seconds
# java -jar ./selenium-server-4.28.1.jar standalone --allow-cors true --session-timeout 999999
# java -jar ./selenium-server-4.28.1.jar -h
# java -jar ./selenium-server-4.28.1.jar standalone -h


# Create a new remote WebDriver session
def create_new_remote_session():
    # Set up Chrome options
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")

    # URL of the remote WebDriver server (e.g., Selenium Grid or a remote machine)
    remote_server_url = "http://localhost:4444/wd/hub"

    # Create a new WebDriver session
    driver = webdriver.Remote(command_executor=remote_server_url, options=options)

    return driver


def get_all_sessions_from_status(grid_url):
    # Make a GET request to the Selenium Grid's /status endpoint
    response = requests.get(f"{grid_url}/status")

    # Parse the JSON response
    status_info = response.json()

    # Extract the sessions information
    nodes = status_info.get("value", {}).get("nodes", [])
    sessions = []
    for node in nodes:
        sessions.extend(node.get("slots", []))

    # Extract session IDs from the slots
    session_ids = [
        slot["session"]["sessionId"] for slot in sessions if slot.get("session")
    ]

    return session_ids


def connect_to_existing_session(server_url, session_id):
    # Create a WebDriver instance using the existing session ID
    original_execute = WebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {"status": 0, "value": None}  # Emulate new session response
        else:
            return original_execute(self, command, params)

    WebDriver.execute = new_command_execute

    options = Options()
    # options.add_experimental_option("detach", True)
    driver = webdriver.Remote(command_executor=server_url, options=options)
    driver.session_id = session_id

    WebDriver.execute = original_execute

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


# open ui http://localhost:4444/ui/
if __name__ == "__main__":
    if not check_port_is_open("localhost", 4444):
        raise RuntimeError(
            '''run the chrome driver in cmd:
              java -jar ./selenium-server-4.28.1.jar standalone --allow-cors true --session-timeout 999999'''
        )

    # Create a new remote session
    driver = create_new_remote_session()

    # Example: Open a website
    driver.get("https://www.example.com")

    # Print the title of the current page
    print(driver.title)

    server_url = "http://localhost:4444"
    # Get the active sessions
    active_sessions = get_all_sessions_from_status(server_url)

    print("Active sessions:", active_sessions)
    # Example server URL and session ID (replace with actual values)
    session_id = active_sessions[0]  # Replace with the session ID you want to connect to
    driver.session_id = active_sessions[0]
    driver.get("https://www.google.com")
    print(driver.title)
    if len(active_sessions) > 1:
        driver.session_id = active_sessions[1]
        driver.get("https://www.trello.com")
        print(driver.title)
