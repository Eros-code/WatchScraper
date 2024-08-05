from bs4 import BeautifulSoup
import io
import os
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def html_getter(url):
    request_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Language":"en-US,en;q=0.9",
                    "Cache-Control": "max-age=0"}

    http = urllib3.PoolManager(headers=request_headers)
    response = http.request("GET", url=url)
    html_bytes = response.data
    html = html_bytes.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def html_getter_with_selenium(url):
    # Set up the Selenium WebDriver (using Chrome in this example)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run headless Chrome
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disables GPU hardware acceleration.
    options.add_argument('--disable-software-rasterizer')  # Disables software rasterizer.
    options.add_argument('--disable-extensions')  # Disable extensions.
    options.add_argument('--disable-logging')  # Disable logging for performance.

    driver = webdriver.Chrome(options=options)

    try:
        # Load the page
        driver.get(url)

        elem = driver.find_element(By.TAG_NAME,"html")
        elem.send_keys(Keys.END)
        time.sleep(5)
        elem.send_keys(Keys.HOME)
        
        driver.implicitly_wait(10)

        SCROLL_PAUSE_TIME = 0.5
        i = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            i += 1
            if "seiko" in url and i == int(soup.find("span", {"class":"_num"}).get_text()):
                break
            if "timex" in url and i == int(soup.find("span", {"class":"js-product-count"}).get_text()[1:-1]):
                break
            if "citizen" or "orient" in url and i == 15:
                break

        print("Page fully loaded, Extracting content...")

        # Get the page source after the dynamic content is loaded
        html = driver.page_source
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        driver.implicitly_wait(10)
        if "seiko" in url:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'a.card-product div._visual img')
            
        elif "citizen" in url:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.object-contain')

        elif "orient" in url:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.product-media img')

        elif "timex" in url:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.product-card__image-wrapper img')

        # Collect src attributes
        image_urls = [x.get_attribute("src") for x in image_elements if x.get_attribute("src")]

        return soup, image_urls
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the WebDriver
        driver.quit()