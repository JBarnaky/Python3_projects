from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui, time, pyperclip, keyboard

driver = webdriver.Firefox(executable_path = "D:\geckodriver-v0.27.0-win64\geckodriver.exe")

driver.get("https://www.youtube.com/")
print(driver.title)

driver.get("https://www.google.com/")
print(driver.title)

time.sleep(5)

driver.back()
print(driver.title)

time.sleep(5)

driver.forward()
print(driver.title)
