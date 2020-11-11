from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox(executable_path = "D:\geckodriver-v0.27.0-win64\geckodriver.exe")

links = driver.find_elements(By.TAG_NAME, "a")

print(len(links))

for link in links:
    print(link.text)

# driver.find_element(By.LINK_TEXT, "Register").click()
# driver.find_element(By.PARTIAL_LINK_TEXT, "Reg").click()

# driver.switch_to_alert().accept()
# driver.switch_to_alert().dismiss()

driver.get("https://www.selenium.dev/selenium/docs/api/java/index.html")

print(driver.current_window_handle)

driver.switch_to.frame("packageListFrame")
driver.find_element_by_link_text("org.openqa.selenium").click()
driver.switch_to.default_content()
time.sleep(3)

driver.switch_to.frame("packageFrame")
driver.find_element_by_link_text("WebDriver").click()
driver.switch_to.default_content()
time.sleep(3)

driver.switch_to.frame("classFrame")
driver.find_element_by_xpath("/html/body/div[1]/ul/li[5]/a").click()
time.sleep(3)

handles = driver.window_handles

for handle in handles:
    driver.switch_to.window(handle)
    print(driver.title)
    if driver.title == "TestValue":
        driver.close()

driver.quit()
