from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from lxml import html


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

# ************************************************************
class Ebay:
    def __init__(self):
        self.url = "https://www.ebay.com/sch/i.html?&_nkw={}"

    def get_page_items(self, tree) -> list:
        container = tree.xpath("//ul[contains(@class, 'srp-results')]")
        if container:
            return container[0].xpath(".//li[contains(@class, 's-item')]")
        else:
            return []

    def create_search_record(self, item):
        title = "".join(item.xpath(".//div[@class='s-item__title']/span/text()"))
        sub_title = "".join(item.xpath(".//div[@class='s-item__subtitle']/text()"))
        sub_title += " " + "".join(
            item.xpath(".//div[@class='s-item__subtitle']//span[@class='SECONDARY_INFO']/text()"))

        rating = "".join(item.xpath(".//div[@class='x-star-rating']//span[@class='clipped']/text()"))
        rating = "None" if not rating else rating

        item_price = item.xpath(".//span[@class='s-item__price']/text()")
        item_price = " to ".join(item_price) if len(item_price) > 1 else "".join(item_price)

        trending_price = "".join(
            item.xpath(".//span[@class='s-item__additional-price']/span[@class='STRIKETHROUGH']/text()"))
        trending_price = "None" if not trending_price else trending_price

        item_link = "".join(item.xpath(".//a[@class='s-item__link']/@href"))
        return title, sub_title, rating, item_price, trending_price, item_link

    def get_next_page(self, tree):
        return "".join(tree.xpath("//a[@class='pagination__next icon-link']/@href"))

    def scrape_ebay(self, keywords: str) -> list:
        url = self.url.format(keywords.replace(" ", "+"))
        response = requests.get(url)

        etree = html.fromstring(response.text)
        page_data = []

        # get remaining pages if existing
        while True:
            items = self.get_page_items(etree)
            if not items:
                break

            for item in items:
                page_data.append(self.create_search_record(item))

            next_page = self.get_next_page(etree)
            if not next_page:
                break

            response = requests.get(next_page)
            if response.status_code != 200:
                break

            etree = html.fromstring(response.text)

        return page_data
