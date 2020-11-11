import sel6
from selenium import webdriver

driver = webdriver.Firefox(executable_path = "D:\geckodriver-v0.27.0-win64\geckodriver.exe")

driver.maximize_window()

driver.get("https://www.youtube.com/")

path = "D:/test.xlsx"

rows = sel6.getRowCount(path, 'Sheet1')

for r in range(2, rows+1):
    username = sel6.readData(path, "Sheet1", r, 1)
    password = sel6.readData(path, "Sheet1", r, 2)

    driver.find_element_by_name("userName").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)

    driver.find_element_by_name("Login").click()

    if driver.title == "someText":
        print("test passed")
        sel6.writeData(path, "Sheet1", r, 3, "test passed")
    else:
        print("test failed")
        sel6.writeData(path, "Sheet1", r, 3, "test failed")

    driver.find_element_by_link_text("Home").click()


