from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from pathlib import Path

BASEURL = 'https://leetcode.com'
PROBLEMSET_URL = '/problemset/all/?difficulty='
TBODY_SELECTOR = (
    By.XPATH,
    '//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[1]',
)
PAGINATION_SELECTOR = (
    By.XPATH,
    '//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span/select',
)
DIFFICULTY = 'Easy'


def fetch_table_source():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(f'{BASEURL}{PROBLEMSET_URL}{DIFFICULTY}')
    driver.maximize_window()

    select = Select(driver.find_element(*PAGINATION_SELECTOR))
    select.select_by_visible_text('all')

    _table = driver.find_element(*TBODY_SELECTOR)
    table_source = _table.get_attribute('innerHTML')

    with open('table_source.html', 'w') as f:
        f.write(table_source)

    driver.quit()


def non_subscription_problems():
    with open(f'leetcode_{DIFFICULTY.lower()}.md', 'w') as outfile:
        outfile.write(f'## {DIFFICULTY}\n\n')
        with open('table_source.html') as infile:
            soup = BeautifulSoup(infile, 'html.parser')
            rows = soup.find_all(['tr'])
            for row in rows:
                cells = row.find_all('td')
                if not (cells[2].find_all('i', {'class': 'fa-lock'})):
                    print(
                        f"[{cells[1].text}: {cells[2]['value']}]({BASEURL}{cells[2].find('a')['href']})"
                    )
                    outfile.write(
                        f"- [{cells[1].text}: {cells[2]['value']}]({BASEURL}{cells[2].find('a')['href']})\n"
                    )
    Path('table_source.html').unlink()

fetch_table_source()
non_subscription_problems()
