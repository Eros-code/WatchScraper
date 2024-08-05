import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapedriver_package import html_getter_with_selenium
from scrapedriver_package import html_getter

timex_url = "https://timex.co.uk/collections/shop-all-watches-new-arrivals?&sort_by=price-ascending"

def timex_watches(timex_url):

    timex_watches = {}
    timex_base_url = "https://www.timex.co,uk"

    timex, timex_image = html_getter_with_selenium(timex_url)

    count = 0
    for link in timex.find_all("li", {"class": "collection-product-grid__list-item"}):
        href = link.find("a")
        model = href["href"].split("-")
        price = link.find("span", {"class": "price-item"}).get_text().replace('\n', '').strip()
        type = href.text.replace('\n', '').strip()
        url = timex_base_url + href['href']
        timex_watches[model[-1]] = {'type':type, 'price': price, 'url':url, 'image':timex_image[count]}
        count += 1
    return timex_watches

print(timex_watches(timex_url))