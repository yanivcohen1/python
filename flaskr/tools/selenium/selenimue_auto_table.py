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

# Wait until the form elements are present time out is 10 sec
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table#customers"))
)
# testing
driver.get("https://www.w3schools.com/html/html_tables.asp")
driver.maximize_window()
# driver.find_element(By.CSS_SELECTOR, "a[href='https://www.neuralnine.com/books/']").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "Books").click()
table_id = driver.find_element(
    By.CSS_SELECTOR,
    "table#customers",
)
# table_id = driver.find_element(By.ID, 'data_configuration_feeds_ct_fields_body0')
rows = table_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
# head = rows[0].text.split(" ")
th = rows[0].find_elements(By.TAG_NAME, "th")
is_head = False
if th:
    is_head = True
for i, row in enumerate(rows):
    if is_head:
        cols = row.find_elements(By.TAG_NAME, "th")
    else:
        cols = row.find_elements(By.TAG_NAME, "td")
    for col in cols:
        print('%30s' % col.text, ",", end=" ")  # prints text from the element
    if is_head:
        print("\n----------------------------------------------------------------------------------------------------")
        is_head = False
    else:
        print()
