import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapedriver_package import html_getter_with_selenium
from scrapedriver_package import html_getter

def max_pages(timex_base_url):
    timex_html = html_getter(timex_base_url)
    number_pages = math.ceil(int(timex_html.find("span", {"class":"js-product-count"}).get_text()[1:-1])/30)
        
    return number_pages

def timex_watches():

    timex_watches = {}

    timex_base_url = "https://timex.co.uk/collections/shop-all-watches-new-arrivals"

    for i in range(1, max_pages(timex_base_url)+1):
        timex_url = timex_base_url + f'?page={i}' + "&sort_by=price-ascending"
        print(f"timex, page {i}")
        print(f"timex url {timex_url}")

        timex, timex_image = html_getter_with_selenium(timex_url)

        count = 0
        for link in timex.find_all("li", {"class": "collection-product-grid__list-item"}):
            href = link.find("a", {"class": "product-card__details-title"})
            model = href["href"].split("-")
            price = link.find("span", {"class": "price-item"}).get_text().replace('\n', '').strip()
            watch_type = href.get_text().replace('\n', '').strip()
            url = timex_base_url + href['href']
            timex_watches[model[-1]] = {'watch_type':watch_type, 'price': price, 'url':url, 'image':timex_image[count]}
            count += 1
    return timex_watches