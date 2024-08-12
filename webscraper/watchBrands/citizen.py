import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapedriver_package import html_getter_with_selenium
from scrapedriver_package import html_getter

def max_pages(citizen_base_url):
    citizen_html = html_getter(citizen_base_url)
    number_pages = citizen_html.find_all("a", {"class": "px-2 py-1 page"})
    pages = []
    for i in number_pages:
        page_number = i.select("span:nth-of-type("+str(2)+")")
        pages.append(page_number[0].text)
    
    number_pages = max(pages)
        
    return number_pages

def citizen_watches():

    citizen_base_url = citizen_url = "https://www.citizenwatch.co.uk/new-arrivals.html"
    citizen_watches = {}

    for i in range(1, int(max_pages(citizen_base_url))):
        if i > 1:
            citizen_url = citizen_base_url + f'?p={i}' + "&product_list_order=price#category-products"
        else:
            citizen_url = citizen_base_url + "?product_list_order=price#category-products"
    
        print(f"citizen, page {i}")
        print(f"citizen url {citizen_url}")

        citizen, citizen_images = html_getter_with_selenium(citizen_url)

        count = 0
        for link in citizen.find_all("form", {"class": "item product product-item product_addtocart_form bg-theme-lightgrey flex flex-col w-full p-2"}):
            price = link.find("span", {"class": "price"}).text.replace('\n', '').strip()
            url = link.find("a", {"class": "product-item-link text-black"})
            watch_type = url.get_text().replace('\n', '').strip()
            citizen_image = citizen_images[count]
            model = link.find("div", {"class":"ruk_rating_snippet"}).get('data-sku')
            citizen_watches[model] = {'watch_type':watch_type, 'price': price, 'url':url['href'], 'image':citizen_image}
            count += 1
    return citizen_watches