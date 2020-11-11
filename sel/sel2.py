from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox(executable_path="D:\geckodriver-v0.27.0-win64\geckodriver.exe")

driver.maximize_window()

driver.get("https://www.google.com/")
driver.implicitly_wait(5)
assert "Google" in driver.title
print(driver.title)

el = driver.find_element_by_name("q")

print(el.is_displayed())
print(el.is_enabled())

el.send_keys("Hololive" + Keys.ENTER)
# driver.find_element_by_name("btnK").click()

driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)
element = wait.until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[4]/form/div[2]/div[1]/div[2]/div/div[2]/input")))

element.click()
element.send_keys(u'\ue009' + u'\ue003')
element.send_keys("youtube" + Keys.ENTER)

inputs = driver.find_elements(By.CLASS_NAME, 'text_field')
print(len(inputs))

status = driver.find_element_by_id("RadioButton").is_selected()
print(status)
driver.find_element_by_id("RadioButton").click()

driver.find_element_by_id("CheckBox").click()

element1 = driver.find_element_by_id("DropDown")
drp = Select(element1)
drp.select_by_visible_text("SomeText_1")
drp.select_by_index(2)
drp.select_by_value("Radio_3")

print(len(drp.options))
all_options = drp.options

for option in all_options:
    print(option.text)
