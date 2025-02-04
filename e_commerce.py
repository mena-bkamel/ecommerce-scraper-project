import re
import time

import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver import Webdriver


def is_valid_price(price: str) -> bool:
    """
    Checks if the provided price string contains a valid price in the format "$<amount>".

    Args:
        price (str): The price string to validate.

    Returns:
        bool: True if the price string is valid and greater than 200, False otherwise.
    """
    try:
        # Use regular expression to match the price format
        match = re.match(r"^\$\d+(?:\.\d+)?$", price)
        if match:
            price_value = float(match.group(0)[1:])
            return price_value > 200
        return False

    except ValueError as e:
        print(f"Error: {e}")
        return False

class Amazon:
    def __init__(self):
        self.base_url = 'https://www.amazon.com'
        self.website_source = "Amazon"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36"
        self.webdriver = Webdriver()
        self.header_row = ["ProductName", "Price", "Rating", "ReviewCount", "Url", "Platform"]

    # filter by price


    def construct_search_url(self, search_text: str) -> str:
        """Construct the search URL for the given search term."""
        search_term = search_text.replace(' ', '+')
        return f'{self.base_url}/s?k={search_term}&ref=cs_503_search'

    def get_next_page_url(self, driver: webdriver.Chrome) -> str | None:
        """Fetch the URL for the next page of search results, if available."""
        try:
            next_button = driver.find_element(by=By.LINK_TEXT, value="Next")
            return next_button.get_attribute("href")
        except NoSuchElementException:
            print("No more pages to scrap.")
            return None

    def extract_record(self, item) -> tuple | str:
        """Extract and return data from a single record"""
        a_tag = item.find('a', class_='a-link-normal s-line-clamp-2 s-link-style a-text-normal')
        url = f"{self.base_url}{a_tag.get('href')}" if a_tag else "N/A"
        name = item.find("h2", {"class": "a-size-medium a-spacing-none a-color-base a-text-normal"}).text

        try:
            price = item.find('span', 'a-price')
            price = price.find('span', 'a-offscreen').text if price else "N/A"
        except AttributeError:
            return "N/A"

        return name, price, url, self.website_source

    def scrape_amazon(self, search_term: str, headless=False) -> list[tuple]:
        """Scrape Amazon for the given search term."""

        records = list()
        url = self.construct_search_url(search_term)
        if headless:
            driver = self.webdriver.initialize_driver(self.user_agent)
        else:
            driver = self.webdriver.setup_headless_driver()

        try:
            driver.get(url)
            while url:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                results = soup.find_all('div', {'data-component-type': 's-search-result'})
                for item in results:
                    record = self.extract_record(item)
                    if is_valid_price(record[1]):
                        records.append(record)

                url = self.get_next_page_url(driver)
                if url:
                    driver.get(url)
                    time.sleep(2)

        except Exception as e:
            print(f"Error during scraping: {e}")

        finally:
            driver.quit()

        return records


class Ebay:
    def __init__(self):
        self.base_url = "https://www.ebay.com/sch/i.html?&_nkw={}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36'
        }
        self.website_source = "Ebay"
        self.header_row = ["ProductName", "SubTiltle", "Rating", "Price", "trendingPrice", "Url", "Platform"]

    def get_page_items(self, tree) -> list:
        return tree.xpath("//ul[contains(@class, 'srp-results')]/li[contains(@class, 's-item')]") or []

    def create_search_record(self, item):

        try:
            title = item.xpath(".//div[@class='s-item__title']/span/text()")
            title = "".join(title).strip() if title else "N/A"

            item_price = item.xpath(".//span[@class='s-item__price']/text()")
            item_price = "".join(item_price[1]) if len(item_price) > 1 else "".join(item_price).strip()

            item_link = item.xpath(".//a[@class='s-item__link']/@href")
            item_link = "".join(item_link).strip() if item_link else "N/A"
            return title, item_price, item_link, self.website_source

        except Exception as e:

            print(f"Error occurred while creating search record: {e}")
            return "N/A", "N/A", "N/A", self.website_source


    def get_next_page(self, tree):
        return "".join(tree.xpath("//a[@class='pagination__next icon-link']/@href")).strip() or None

    def scrape_ebay(self, keywords: str) -> list:
        search_url = self.base_url.format(keywords.replace(" ", "+"))
        page_data = list()

        while search_url:
            try:
                response = requests.get(search_url, timeout=50)
                response.raise_for_status()
                etree = html.fromstring(response.text)
                items = self.get_page_items(etree)

                for item in items:
                    record = self.create_search_record(item)
                    if record:
                        if is_valid_price(record[1]):
                            page_data.append(record)

                search_url = self.get_next_page(etree)
                print(search_url)
            except requests.RequestException as e:
                print(f"Error fetching URL {search_url}: {e}")
                continue
        return page_data


class Target:
    def __init__(self):
        self.URL = "https://www.target.com/s?searchTerm={}"
        self.website_source = "Target"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36"
        self.webdriver = Webdriver()
        self.header_row = ["ProductName", "Price", "Rating", "Url", "Platform"]


    def get_page_items(self, tree) -> list:
        container = tree.xpath("//section[contains(@class, 'sc-e0eaa558-1 haoIOG')]")
        if container:
            return container[0].xpath(".//div[@class='sc-5da3fdcc-0 ksJpxP']/div")
        else:
            return []

    def create_search_record(self, item):
        try:
            name = item.xpath(".//div[@class='styles_truncate__Eorq7 sc-4d32bc34-0 kkvIvZ']/text()")
            name = "".join(name).strip() if name else "N/A"

            price = item.xpath(".//span[@data-test='current-price']/span/text()")
            price = "".join(price).strip() if price else "N/A"

            url_part = item.xpath(".//a[@class='sc-e851bd29-0 sc-f76ad31b-1 hNVRbT dpaMdN h-display-block']/@href")
            url_part = "".join(url_part).strip() if url_part else "N/A"
            url = f"https://www.target.com{url_part}" if url_part and url_part.startswith("/") else url_part

            return name, price, url, self.website_source

        except Exception as e:
            print(f"Error occurred while creating search record: {e}")
            return "N/A", "N/A", "N/A", self.website_source


    def scroll_the_page(self, driver, scroll_amount=200):
        scroll_amount = scroll_amount
        while True:
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(0.2)
            scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
            page_height = driver.execute_script("return document.body.scrollHeight")
            if scroll_position >= page_height:
                break

    def get_number_of_pages(self, tree) -> int:
            num_pages = "".join(tree.xpath('//*[@id="select-custom-button-id"]/span/text()')).split()[3]
            return int(num_pages)

    def scrape_target(self, keywords: str):
        url = self.URL.format(keywords.replace(" ", "-"))
        driver = self.webdriver.initialize_driver(self.user_agent)
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div")))
        self.scroll_the_page(driver)
        tree = html.fromstring(driver.page_source)
        page_data = list()
        num_pages = self.get_number_of_pages(tree)
        nao_query = 0

        for num in range(num_pages):
            items = self.get_page_items(tree)
            if not items:
                break

            for item in items:
                record = self.create_search_record(item)
                if record[0] or record[1]:
                    page_data.append(record)

            if num >= (num_pages - 1):
                driver.close()
                break

            nao_query += 24
            driver.get(f"{url}&Nao={nao_query}")
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div")))
            self.scroll_the_page(driver)
            tree = html.fromstring(driver.page_source)

        return page_data



