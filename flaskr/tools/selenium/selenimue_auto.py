import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
current_folder = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(current_folder, "chromedriver.exe")
# chrome_install = ChromeDriverManager().install()
# folder = os.path.dirname(chrome_install)
# chromedriver_path = os.path.join(folder, "chromedriver.exe")
service = Service(chromedriver_path)
driver = webdriver.Chrome(
    service=service, options=options
)
driver.get("https://www.neuralnine.com/")
# driver.maximize_window()
# Wait until the form elements are present time out is 10 sec
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href]"))
)
# driver.find_element(By.CSS_SELECTOR, "a[href='https://www.neuralnine.com/books/']").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "Books").click()
links = driver.find_elements(By.XPATH, "//a[@href]")
for link in links:
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break
