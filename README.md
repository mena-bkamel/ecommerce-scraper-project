# E-commerce Scraper

**Overview**

The E-commerce Scraper is a Python-based tool designed to scrape product details from multiple e-commerce platforms, including Amazon and eBay. This project efficiently collects product names, prices, URLs, and platform details, storing the data in CSV, JSON, and SQLite databases.

This scraper can be beneficial for price monitoring, competitor analysis, and market research, making it a valuable tool for freelancers and businesses looking to track e-commerce trends.

**Features**

* Scrapes Amazon and eBay for product details.
* Stores data in multiple formats (CSV, JSON, SQLite database).
* Supports pagination for comprehensive data collection.
* Uses Selenium and BeautifulSoup for web scraping.
* Customizable search queries for different products.
* Handles errors and exceptions to ensure stability.

**Technologies Used**

* Python
* Selenium – for web scraping with dynamic content handling.
* BeautifulSoup & lxml – for HTML parsing.
* Requests – for handling HTTP requests.
* SQLite – for structured database storage.
* CSV & JSON – for flexible data export.

**Installation**

**Prerequisites**

* Ensure you have the following installed:
    * Python 3.8+
    * Google Chrome & Chromedriver (for Selenium)

**Required Python libraries:**

```bash
pip install selenium beautifulsoup4 lxml requests sqlite3
