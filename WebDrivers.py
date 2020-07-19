from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WebDrivers:
    def chrome_driver():
        chrome_options = Options()
        CHROMEDRIVER_PATH = "../bin/SeleniumWebDrivers/chromedriver"
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
        return driver

    def firefox_driver():
        driver = webdriver.Firefox()
        return driver

