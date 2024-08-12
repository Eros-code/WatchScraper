import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapedriver_package import html_getter_with_selenium
from scrapedriver_package import html_getter

def max_pages(orient_url):
    orient_html = html_getter(orient_url)
    number_pages = orient_html.find("span", {"class": "pagination-count__page-count"}).text[-1]
    return number_pages

def orient_watches():
    orient_url = "https://www.orientwatch.co.uk/or/en_GB/products/watches/c/watches?q=%3Aprice-asc&page=0"
    orient_watches = {}
    orient_base_url = "https://www.orientwatch.co.uk"

    for i in range(0, int(max_pages(orient_url))):
        print(f"orient, page {i}")
        orient_url = orient_url[:-1] + str(i)
        print(orient_url)
        orient, orient_image = html_getter_with_selenium(orient_url)

        count = 0
        for link in orient.find_all("a", {"class": "product-card__link"}):
            model = link.find("div", {"class": "product-card__code"}).text.replace('\n', '').strip()
            price = link.find("div", {"class": "product-pricing__price"}).text.replace('\n', '').strip()
            watch_type = link.find("h3", {"class": "product-card__name"}).text.replace('\n', '').strip()
            url = orient_base_url + link['href']
            orient_watches[model] = {'watch_type':watch_type, 'price': price, 'url':url, 'image':orient_image[count]}
            count += 1
    return orient_watches