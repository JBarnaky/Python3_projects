import unittest
from selenium import webdriver

class SearchEnginesTest(unittest.TestCase):
    def test_Google(self):
        self.driver = webdriver.Firefox(executable_path="D:\geckodriver-v0.27.0-win64\geckodriver.exe")
        self.driver.get("https://www.google.com/")
        print(self.driver.title)
        self.driver.close()

    def test_Bing(self):
        self.driver = webdriver.Firefox(executable_path="D:\geckodriver-v0.27.0-win64\geckodriver.exe")
        self.driver.get("https://www.bing.com/")
        print(self.driver.title)
        self.driver.close()

    if __name__ == "__main__":
        unittest.main()