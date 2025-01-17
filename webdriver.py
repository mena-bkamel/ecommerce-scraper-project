from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class Webdriver:
    def __init__(self):
        self.chromedriver_path = r"F:\chromedriver-win64\chromedriver.exe"

    def chrome_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome()
        return driver

    def setup_headless_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Required for Linux environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid resource issues
        chrome_options.add_argument("--window-size=1920,1080")  # Set default window size

        # Path to chromedriver executable
        driver_service = Service(self.chromedriver_path)
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
        return driver

