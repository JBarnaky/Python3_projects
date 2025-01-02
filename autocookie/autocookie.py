from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Firefox(executable_path=r'D:\geckodriver-v0.35.0-win-aarch64\geckodriver.exe')

try:
    driver.get("https://orteil.dashnet.org/cookieclicker/")
    driver.set_page_load_timeout(5)
    print(driver.title)

    driver.implicitly_wait(1)

    cookie = driver.find_element(By.ID, "bigCookie")
    cookie_count = driver.find_element(By.ID, "cookies")

    while True:
        actions = ActionChains(driver)
        actions.click(cookie)
        actions.perform()

        count = int(cookie_count.text.split(" ")[0])

        items = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(1, -1, -1)]
        for item in items:
            value = int(item.text)
            if value <= count:
                upgrade_actions = ActionChains(driver)
                upgrade_actions.move_to_element(item)
                upgrade_actions.click()
                upgrade_actions.perform()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
