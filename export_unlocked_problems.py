from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import atexit

BASEURL = "https://leetcode.com"
TOP_PROBLEMSET_URL = "/problemset/top-interview-questions/?difficulty="
ALL_PROBLEMSET_URL = "/problemset/all/?difficulty="
TBODY_SELECTOR = (
    By.XPATH,
    '//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[1]',
)
PAGINATION_SELECTOR = (
    By.XPATH,
    "//span/select[@class='form-control']",
)
DIFFICULTY = "Easy"


class LeetCodeParser:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(f"{BASEURL}")
        self.driver.maximize_window()
        atexit.register(self._quit)

    def _select_no_paginate(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(PAGINATION_SELECTOR)
        )
        select = Select(self.driver.find_element(*PAGINATION_SELECTOR))
        select = Select(self.driver.find_element(*PAGINATION_SELECTOR))
        select.select_by_visible_text("all")

    def fetch_top_problems(self):
        """
        Get a list of https://leetcode.com/problemset/top-interview-questions
        """
        self.driver.get(f"{BASEURL}{TOP_PROBLEMSET_URL}{DIFFICULTY}")
        self._select_no_paginate()
        _table = self.driver.find_element(*TBODY_SELECTOR)
        _rows = _table.find_elements(By.TAG_NAME, "tr")
        _top_problems = []
        for row in _rows:
            _ = row.find_elements(By.TAG_NAME, "td")[1]
            _top_problems.append(_.text)
        return _top_problems

    def fetch_all_unlocked_problems(self):
        """
        Fetch all unlocked problems
        """
        self.driver.get(f"{BASEURL}{ALL_PROBLEMSET_URL}{DIFFICULTY}")
        self._select_no_paginate()
        _table = self.driver.find_element(*TBODY_SELECTOR)
        return _table.get_attribute("innerHTML")

    def parse_and_write_output(self):
        __top_problems = self.fetch_top_problems()
        __all_problems_table_source = self.fetch_all_unlocked_problems()
        with open(f"leetcode_{DIFFICULTY.lower()}.md", "w") as outfile:
            outfile.write(f"## {DIFFICULTY}\n\n")
            soup = BeautifulSoup(__all_problems_table_source, "html.parser")
            rows = soup.find_all(["tr"])
            for row in rows:
                cells = row.find_all("td")
                if not (cells[2].find_all("i", {"class": "fa-lock"})):
                    if cells[1].text in __top_problems:
                        outfile.write(
                            f"- [**{cells[1].text}: {cells[2]['value']}**]({BASEURL}{cells[2].find('a')['href']})\n"
                        )
                    else:
                        outfile.write(
                            f"- [{cells[1].text}: {cells[2]['value']}]({BASEURL}{cells[2].find('a')['href']})\n"
                        )

    def _quit(self):
        self.driver.quit()


lc = LeetCodeParser()
lc.parse_and_write_output()
