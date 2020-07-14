import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('../bin/chromedriver')
#driver.get("https://www.python.org")
#driver.get("https://www.chess.com")
driver.get("https://www.chess.com/login_and_go")
elem = driver.find_element_by_id("username")
elem.send_keys("fun_man")
elem = driver.find_element_by_id("password")
elem.send_keys("chessflares")
elem.send_keys(Keys.RETURN)
c = 0

url = "https://www.chess.com/games/archive/fun_man"
url = "https://www.chess.com/games/archive/fun_man?gameOwner=other_game&gameType=recent&endDate%5Bdate%5D=07%2F10%2F2020&startDate%5Bdate%5D=07%2F06%2F2020&timeSort=desc"
url = "https://www.chess.com/games/archive?gameOwner=my_game&gameType=recent&endDate%5Bdate%5D=07%2F05%2F2020&startDate%5Bdate%5D=06%2F23%2F2020&timeSort=desc"

url = "https://www.chess.com/games/archive?gameOwner=my_game&gameType=recent&endDate%5Bdate%5D=06%2F23%2F2020&startDate%5Bdate%5D=06%2F15%2F2020&timeSort=desc"

url = "https://www.chess.com/games/archive?gameOwner=my_game&gameType=recent&endDate%5Bdate%5D=06%2F15%2F2020&startDate%5Bdate%5D=06%2F08%2F2020&timeSort=desc"

while True:
    driver.get(url)
    main_window = driver.current_window_handle

    driver.execute_script("window.scrollTo(0, 500)")
    c = c + 1
    print("Clicking Analyse Game...", c)
    elems = driver.find_elements_by_class_name("archive-games-link")
    i = 0
    open_tab = 0
    for elem in elems:
        if i == 8:
            break
        i = i + 1
        print(elem.text)
        if elem.text == "Analyze":
            elem.send_keys(Keys.COMMAND + Keys.RETURN)
            open_tab = open_tab + 1

    if open_tab == 0:
        print("No more analysis links found.. terminating")
        exit(0)
    """
    links = [elem.get_attribute('href') for elem in elems]
    print(links)
    i = 1
    for link in links:
        if "analysis" in link:
            driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND+ Keys.TAB)
            i = i + 1
        if i == 5:
            break
    time.sleep(5)
    browser.switch_to_window(main_window)
    """

    print(driver.window_handles)

    # Close all tabs
    time.sleep(20)
    def close_all_windows_except_first():
        for tab in driver.window_handles:
            if tab != main_window:
                driver.switch_to_window(tab)
                driver.close()
        driver.switch_to_window(main_window)

    close_all_windows_except_first()

    #elem = driver.find_element_by_class_name("modal-close")
    print("Sleeping 20 seconds")
    time.sleep(2)
