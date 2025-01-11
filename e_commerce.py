from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from store_data import Data


class Amazon:
    def __init__(self):
        self.url = 'https://www.amazon.com'

    def chrome_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=chrome_options)

        return driver

    def get_url(self, search_text: str):
        """Generate a url from search text"""
        template = f'{self.url}/s?k={{}}&ref=cs_503_search'
        search_term = search_text.replace(' ', '+')
        # add term query to url
        url = template.format(search_term)

        return url

    def search_for_product(self, driver: chrome_webdriver, search_term):
        search_bar = driver.find_element(By.ID, "e")
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

    def next_page(self, driver: chrome_webdriver):
        try:
            a_tag = driver.find_element(by=By.LINK_TEXT, value="Next")
            url = f"{a_tag.get_attribute("href")}"
            return url
        except NoSuchElementException:
            print("No More pages to scrap")
            driver.close()
            return None

    def extract_record(self, item):
        """Extract and return data from a single record"""

        # description and url
        a_tag = item.find('a', class_='a-link-normal s-line-clamp-2 s-link-style a-text-normal')
        url = f"{self.url}{a_tag.get('href')}"
        description = item.h2.text

        try:
            # product price
            price_parent = item.find('span', 'a-price')
            price = price_parent.find('span', 'a-offscreen').text

        except AttributeError:
            return

        try:
            # rating and review count
            rating = item.i.text
            review_count = item.find('span', {'class': 'a-size-base s-underline-text'}).text

        except AttributeError:
            rating = ''
            review_count = ''

        result = (description, price, rating, review_count, url)

        return result

    def scrape_amazon(self, search_term) -> list[tuple]:

        records = []
        url = self.get_url(search_term)
        driver = self.chrome_webdriver()

        driver.get(url)
        self.search_for_product(driver, search_term)

        next_page_url = self.next_page(driver)

        while next_page_url:

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            results = soup.find_all('div', {'data-component-type': 's-search-result'})
            for item in results:
                record = self.extract_record(item)
                if record:
                    records.append(record)

            driver.get(next_page_url)
            next_page_url = self.next_page(driver)

        return records
