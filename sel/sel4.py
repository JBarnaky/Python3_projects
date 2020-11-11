from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

fp=webdriver.FirefoxProfile()
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,application/pdf")
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "C:\DownloadedFiles")
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(executable_path = "D:\geckodriver-v0.27.0-win64\geckodriver.exe", firefox_profile=fp)

driver.maximize_window()

driver.get("https://www.youtube.com/")

driver.execute_script("window.scrollBy(0,1000)", "")

flag = driver.find_element_by_xpath("//xpath")
driver.execute_script("arguments[0].scrollIntoView();", flag)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

actions = ActionChains(driver)
element = driver.find_element_by_xpath("//xpath")

actions.move_to_element(element).move_to_element().move_to_element().click().perform()

actions.double_click(element).perform() #double_lmb

actions.context_click(element).perform() #rmb

actions.drag_and_drop("source", "target").perform()
