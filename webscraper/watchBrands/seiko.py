import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapedriver_package import html_getter_with_selenium
from scrapedriver_package import html_getter
from scrapedriver_package import initial_page_load

def max_pages(seiko_html):
    initial_div = seiko_html.find("div", {"class", "watchfinder-utility"})
    number_pages = math.ceil(int(initial_div.find("span", {"class":"_num"}).get_text().replace('\n', "").strip())/20)
    return number_pages

def seiko_watches():
    seiko_url = 'https://www.seikowatches.com/uk-en/watchfinder?new=true&sort=LowSortByPrice'
    initial_seiko = initial_page_load(seiko_url)
    seiko_max_pages = max_pages(initial_seiko)
    seiko_max_page_url = seiko_url + f'&page={seiko_max_pages}'
    seiko, seiko_image = html_getter_with_selenium(seiko_max_page_url)

    print("Seiko html page scraped")

    seiko_watches = {}
    seiko_base_url = "https://www.seikowatches.com"
    count = 0
    for link in seiko.find_all("a", {"class": "card-product"}):
        model = link['href'].split('/')
        price = link.find("div", {"class": "_price"}).text
        url = seiko_base_url + link['href']
        seiko_watches[model[-1]] = {'watch_type':model[-2], 'price': price, 'url':url, 'image':seiko_image[count]}
        count += 1
    return seiko_watches