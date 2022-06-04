import json
from math import prod
import time
import requests
import os
from bs4 import BeautifulSoup
import random
ROOT_OF_DATABASE = f'{os.path.dirname(__file__)}/database.json'


database = json.load(open(ROOT_OF_DATABASE,encoding='utf8'))


class Product():
    def __init__(self, title, price, description, image, category, characteristics):
        self.title = title
        self.price = price
        self.description = description
        self.image = image
        self.category = category
        self.count = random.randint(1, 50)
        self.characteristics = characteristics

class Parser():
    BASE_URL = "https://megastroy.kz"

    MARKET_URL = f"{BASE_URL}/astana/market/stroitelnye-materialy/"

    stroi_materiali = [
    'stroitelstvo-sten-i-peregorodok/','gipsokarton-i-komplektuyushie/','paneli-stenovye-i-komplektuyushie/','stroitelnye-setki/', 'stroitelnaya-izolyaciya/',
    'elementy-dekora/','lestnichnye-elementy/','kovanye-elementy/']

    def get_products_container(self, soup):
        return soup.find("div", {'class':'productsCategoryContainer'})
    
    def get_products(self, soup_of_products):
        return soup_of_products.find_all('div', {'class': 'recProductItem'})
    
    def get_link(self, soup_of_products):
        result = list()
        for soup in soup_of_products:
            result.append(soup.find('a', {'class': 'recProductItem__name'}).get('href'))
        return result
    
    def get_title(self, soup_of_product):
        return soup_of_product.find('div',{'class': 'rightCol col-xs-12 col-lg-6 col-md-12 pull-right'}).find('h2').text

    def get_price(self, soup_of_product):
        return self.extract_digits(soup_of_product.find('div',{'class': 'poCurrentPrice'}).text)
    
    def get_description(self, soup_of_product):
        return soup_of_product.find('div', {'class': 'poDescription col-lg-12'}).text.replace('\n', '<br>')

    def extract_digits(self, string):
        num = ""
        for c in string:
            if c.isdigit():
                num = num + c
        return int(num)

    def get_characteristic(self, soup_of_product):
        rows = soup_of_product.find('table', {'class': 'table table-striped'}).find_all('tr')
        characteristics = dict()
        for row in rows:
            tds = row.find_all('td')
            characteristics[tds[0].text] = tds[1].text.strip()
        return characteristics

    def get_content_of(self, url):
        print(f"Getting content of {url}")
        return requests.get(f'{url}').content
        
    def get_image_link(self, soup_of_product):
        return self.BASE_URL + soup_of_product.find('div', {'class':'imageBox'}).find('img').get('src')
    
    def download_image(self, link_to_img):
        response = requests.get(link_to_img)
        name = link_to_img.split('/')[-1]
        file = open(f"C:/Users/Адиль/Desktop/AITU/paidProjects/stroiMart/stroimarket/main/static/main/images/products/{name}", "wb")
        file.write(response.content)
        file.close()
        print("Successfully downloaded")
        return name

    def start(self):
        for catalog in self.stroi_materiali:
            content = self.get_content_of(self.MARKET_URL + catalog)
            self.soup = BeautifulSoup(content, 'html.parser')
            links = self.get_link(self.get_products(self.get_products_container(self.soup)))
            for link in links:
                content = self.get_content_of(f'{self.BASE_URL}/{link}')
                soup_of_product = BeautifulSoup(content, 'html.parser')

                title = self.get_title(soup_of_product)
                price = self.get_price(soup_of_product)
                description = self.get_description(soup_of_product)
                characteristics = self.get_characteristic(soup_of_product)
                name_of_image = self.download_image(self.get_image_link(soup_of_product))

                product = Product(title, price, description, name_of_image, catalog.replace('/',''), characteristics)
                database.append(product.__dict__)
                json.dump(database,open(ROOT_OF_DATABASE,'w',encoding='utf-8'), indent=2, ensure_ascii=False)
                print(product.__dict__)
                time.sleep(0.2)
            time.sleep(2)



parser = Parser()
parser.start()
# counter = 0
# for idiom in database:
#     if idiom['description']!=None:
#         counter += 1
# print(counter)

        
    