import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapedriver_package import html_getter_with_selenium
from scrapedriver_package import html_getter


def seiko_watches():
    seiko_url = seiko_url = 'https://www.seikowatches.com/uk-en/watchfinder?new=true&page=2'

    seiko, seiko_image = html_getter_with_selenium(seiko_url)

    seiko_watches = {}
    seiko_base_url = "https://www.seikowatches.com"
    count = 0
    for link in seiko.find_all("a", {"class": "card-product"}):
        model = link['href'].split('/')
        price = link.find("div", {"class": "_price"}).text
        url = seiko_base_url + link['href']
        seiko_watches[model[-1]] = {'type':model[-2], 'price': price, 'url':url, 'image':seiko_image[count]}
        count += 1
    return seiko_watches

print(seiko_watches())