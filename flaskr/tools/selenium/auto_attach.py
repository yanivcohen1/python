from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
from flaskr.tools.selenium.get_selenium_driver import connect_to_driver
# you need first to run the chrome driver in cmd (.\chromedriver.exe --port=5000)

# 1. open a driver
# driver = webdriver.Chrome(options=options)
# 2. extract to session_id and _url from driver object.
# url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
# session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
# 3. Use these two parameter to connect to your driver.
options = Options()
options.add_argument("--start-maximized")
# driver = webdriver.Chrome(options=options)
port = 5000
url = "http://127.0.0.1:" + str(port) # driver.command_executor._url
options.add_experimental_option("detach", True)
# url = "http://localhost:9515"
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
    print(driver.current_url)
    driver.session_id = new_session_id
    # this prevents the dummy browser
    driver.close()
    driver.session_id = session_id
except:
    driver.session_id = new_session_id
    with open(FILE_NAME, "w") as f:
        f.write(driver.session_id)
print(driver.session_id)

# testing
driver.get("https://www.neuralnine.com/")
# driver.maximize_window()
# driver.find_element(By.CSS_SELECTOR, "a[href='https://www.neuralnine.com/books/']").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "Books").click()
links = driver.find_elements(By.XPATH, "//a[@href]")
for link in links:
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break
