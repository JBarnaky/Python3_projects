from selenium import webdriver

driver = webdriver.Firefox(executable_path = "D:\geckodriver-v0.27.0-win64\geckodriver.exe")

driver.maximize_window()

driver.get("https://www.youtube.com/")

cookies = driver.get_cookies()
print(len(cookies))
print(cookies)

cookie = {'name': 'Mycookie', 'value': '1234567890'}
driver.add_cookie(cookie)

driver.delete_all_cookies()
print(len(cookies))
print(cookies)

driver.save_screenshot("D:/scr.jpg")
driver.get_screenshot_as_file("D:/scr.png")

