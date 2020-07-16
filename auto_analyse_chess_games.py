import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from getChessURLs import ChessArchiveUrlGenerator
from datetime import date
from selenium.webdriver.chrome.options import Options

options = Options()
#options.headless = True
CHROMEDRIVER_PATH = "../bin/chromedriver"
CHROMEDRIVER_PATH = "../bin/SeleniumWebDrivers/geckodriver"
#driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
driver = webdriver.Firefox()

#driver.get("https://www.chess.com")
driver.get("https://www.chess.com/login_and_go")
elem = driver.find_element_by_id("username")
elem.send_keys("fun_man")
#elem.send_keys("7whatsthat")
elem = driver.find_element_by_id("password")
elem.send_keys("chessflares")
#elem.send_keys("whatsthat")
elem.send_keys(Keys.RETURN)
c = 0

url = "https://www.chess.com/games/archive/fun_man"
url = "https://www.chess.com/games/archive/fun_man?gameOwner=other_game&gameType=recent&endDate%5Bdate%5D=07%2F10%2F2020&startDate%5Bdate%5D=07%2F06%2F2020&timeSort=desc"
url = "https://www.chess.com/games/archive?gameOwner=my_game&gameType=recent&endDate%5Bdate%5D=07%2F05%2F2020&startDate%5Bdate%5D=06%2F23%2F2020&timeSort=desc"

url = "https://www.chess.com/games/archive?gameOwner=my_game&gameType=recent&endDate%5Bdate%5D=06%2F23%2F2020&startDate%5Bdate%5D=06%2F15%2F2020&timeSort=desc"

url = "https://www.chess.com/games/archive?gameOwner=my_game&gameType=recent&endDate%5Bdate%5D=06%2F15%2F2020&startDate%5Bdate%5D=06%2F08%2F2020&timeSort=desc"

url_gen = ChessArchiveUrlGenerator()
url_gen.reset(date(2020,4,16), date(2020,6,1))

url = url_gen.getNextUrl()
print ("Got this url -> ", url)

def close_all_windows_except_first(driver, main_window):
    for tab in driver.window_handles:
        if tab != main_window:
            driver.switch_to_window(tab)
            driver.close()
    driver.switch_to_window(main_window)

def open_new_tabs(driver):
    elems = driver.find_elements_by_class_name("archive-games-link")
    i = 0
    open_tab = 0
    for elem in elems:
        if i == 2:
            break
        i = i + 1
        if elem.text == "Analyze":
            print(elem.text, elem.get_attribute('href'))
            elem.send_keys(Keys.COMMAND + Keys.RETURN)
            open_tab = open_tab + 1
    return open_tab

while True:
    driver.get(url)
    main_window = driver.current_window_handle

    driver.execute_script("window.scrollTo(0, 500)")
    c = c + 1
    print("Clicking Analyse Game...", c)
    open_tab = open_new_tabs(driver)

    if open_tab == 0:
        print("No more analysis links found.. changing url")
        url = url_gen.getNextUrl()
        if url == None:
            exit()
        continue

    print(driver.window_handles)

    print("Sleeping 20 seconds")
    time.sleep(60)

    print("Closing tabs..")
    close_all_windows_except_first(driver, main_window)

    print("Sleeping 2 seconds")
    time.sleep(2)
