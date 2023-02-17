import time
import selenium
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdrivermanager import ChromeDriverManager


class TestChromeCases():
    # desired_capabilities = {'browserName': 'chrome'}
    # driver = webdriver.Remote(
    #     command_executor='http://192.168.5.12:4444/wd/hub',
    #     desired_capabilities=desired_capabilities
    # )
    driver = webdriver.Chrome(executable_path="C:\\Users\\ANIRUDDHA\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe")

    def test_sample_one(self):
        self.driver.get("https://www.google.com")
        self.driver.find_element(By.NAME, "q").send_keys("Selenium Java Tutorial")
        title = self.driver.title
        print(title)

    def test_sample_two(self):
        self.driver.get("https://www.youtube.com")
        self.driver.find_element(By.XPATH, "//input[@id='search']").send_keys("Selenium Java Tutorial")
        title = self.driver.title
        print(title)
