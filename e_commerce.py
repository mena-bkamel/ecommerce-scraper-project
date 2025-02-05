import re
import time

import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By

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
        self.header_row = ["ProductName", "Price", "Url", "Platform"]

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
                    if record:
                        records.append(record)

                url = self.get_next_page_url(driver)
                if url:
                    driver.get(url)
                    time.sleep(2)

        except Exception as e:
            print(f"Error during scraping: {e}")
            self.scrape_amazon(search_term, headless=headless)

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
        self.header_row = ["ProductName", "Price", "Url", "Platform"]

    def get_page_items(self, tree) -> list:
        return tree.xpath("//ul[contains(@class, 'srp-results')]/li[contains(@class, 's-item')]") or []

    def create_search_record(self, item):
        try:
            # Extract the title
            title = item.xpath(".//div[@class='s-item__title']/span/text()")
            title = "".join(title).strip() if title else "N/A"

            # Extract the price(s)
            item_price = item.xpath(".//span[@class='s-item__price']/text()")
            item_price = "".join(item_price[0]) if len(item_price) > 1 else "".join(item_price).strip()

            # Extract the item link
            item_link = item.xpath(".//a[@class='s-item__link']/@href")
            item_link = "".join(item_link).strip() if item_link else "N/A"

            return title, item_price, item_link, self.website_source

        except Exception as e:
            # Log the error and return default values
            print(f"Error occurred while creating search record: {e}")
            return "N/A", "N/A", "None", "None", "N/A", self.website_source
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
                        if record:
                            page_data.append(record)

                search_url = self.get_next_page(etree)
                print(search_url)
            except requests.RequestException as e:
                print(f"Error fetching URL {search_url}: {e}")
                continue
        return page_data

