import time
from getChessURLs import ChessArchiveUrlGenerator
from datetime import date
from WebDrivers import WebDrivers
from selenium.webdriver.common.keys import Keys

MAX_ITERATIONS = 80
SLEEP_TIME = 30
MAX_ACTIVE_TABS = 12

class ChessDotComHandler:
    def __init__(self):
        self.driver = WebDrivers.chrome_driver()
        self.url_gen = ChessArchiveUrlGenerator()
        self.url_gen.reset(date(2020,4,18), date(2020,7,15))
        self.terminate_main_loop = False

        self.accounts = {
                "fun_man": {"username" : "fun_man", "password" : "chessflares"},
                "7whatsthat": {"username" : "7whatsthat", "password" : "whatsthat"}
                }

    def run(self):
        try:
            self.mainLoop()
        finally:
            self.driver.quit()

    def mainLoop(self):
        self.login_to_chesscom(self.accounts["fun_man"])

        self.active_archive_url = self.url_gen.getNextUrl()
        for i in range(MAX_ITERATIONS):
            if not self.terminate_main_loop:
                self.check_chess_arhives_page()
                import code
                code.interact(local=locals())
            else:
                self.driver.close()

    def login_to_chesscom(self, account):
        self.driver.get("https://www.chess.com/login_and_go")

        elem = self.driver.find_element_by_id("username")
        elem.send_keys(account["username"])
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(account["password"])

        elem.send_keys(Keys.RETURN)

    def check_chess_arhives_page(self):
        if self.active_archive_url == None:
            self.terminate_main_loop = True
            return

        self.driver.get(self.active_archive_url)

        main_window = self.driver.current_window_handle

        num_tabs_open = self.open_new_analyse_tabs()

        if num_tabs_open == 0:
            print("No more analysis links found in this page.. changing url")
            self.active_archive_url = self.url_gen.getNextUrl()
            if self.active_archive_url== None:
                self.terminate_main_loop = True
            return

        print("Sleeping %s seconds" %SLEEP_TIME)
        time.sleep(SLEEP_TIME)

        self.close_all_windows(except_windows = [main_window])

    def open_new_analyse_tabs(self):
        elems = self.driver.find_elements_by_class_name("archive-games-link")
        i = 0
        num_open_tabs = 0
        for elem in elems:
            if i == MAX_ACTIVE_TABS:
                break
            i = i + 1
            if elem.text == "Analyze":
                print(elem.text, elem.get_attribute('href'))
                elem.send_keys(Keys.COMMAND + Keys.RETURN)
                num_open_tabs = num_open_tabs + 1
        print(self.driver.window_handles)
        return num_open_tabs

    def close_all_windows(self, except_windows = []):
        for tab in self.driver.window_handles:
            if tab not in except_windows:
                self.driver.switch_to_window(tab)
                self.driver.close()
        if len(except_windows):
            self.driver.switch_to_window(except_windows[0])

if __name__ == "__main__":
    handler = ChessDotComHandler()
    handler.run()
