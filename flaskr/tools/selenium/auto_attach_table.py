from flaskr.tools.selenium.get_selenium_driver import connect_to_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# you need first to run the chrome driver in cmd (.\chromedriver.exe --port=5000)

# 1. open a driver
# driver = webdriver.Chrome(options=options)
# 2. extract to session_id and _url from driver object.
# url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
# session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
# 3. Use these two parameter to connect to your driver.
driver = connect_to_driver()
driver.get("https://www.w3schools.com/html/html_tables.asp")

# Wait until the form elements are present time out is 10 sec
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table#customers"))
)
# testing
#   driver.maximize_window()
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
        print(
            f"{col.text:>30} ,", end=" "
        )  # cell string should be right-aligned (>) and take up 30 characters in width
    if is_head:
        print(
            "\n----------------------------------------------------------------------------------------------------"
        )
        is_head = False
    else:
        print()
