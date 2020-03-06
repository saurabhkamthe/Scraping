import requests
import json
from bs4 import BeautifulSoup
import re

product = 'mobiles'     #product you want to scrap the data for
response = requests.get('https://www.flipkart.com/search?q=' + product)
#print(response.content)

r_data = BeautifulSoup(response.content, 'lxml')

d_data = r_data.find_all('div', {'class' : 'bhgxx2 col-12-12'})
links_list = []
for i in d_data:
    try:
        a = i.find('a')
        a = i.find('a', {'calss' : a})
        links_list.append(a.get('href'))
    except:
        pass

json_list = []              #to store the urls of all the products on the result page
for link in links_list:
    try:                     #exception handling as some of the links are broken
        response = requests.get('https://www.flipkart.com' + link)
        #print(response.content)

        r_data = BeautifulSoup(response.content, 'lxml')

        #print(r_data)

        d_data = r_data.find('div', {'class' : '_1HmYoV hCUpcT'})

        img_data = d_data.find_all('div', {'class' : '_2_AcLJ'})
        img = []
        for i in img_data:
            u = re.match('.*\((.*)\)', i.get('style'))
            img.append(u.group(1))
        #print(img)

        ratings = d_data.find('div', {'class' : 'hGSR34'})
        ratings = ratings.get_text()
        #print(ratings)

        reviews = d_data.find('span', {'class' : '_38sUEc'})
        reviews = reviews.get_text().split()[3]
        #print(reviews)

        price = d_data.find('div', {'class' : '_1vC4OE _3qQ9m1'})
        price = price.get_text()[1:]
        #print(price)

        details = d_data.find_all('div', {'class' : '_2RngUh'})
        for i in details:
            if 'Product Details' in i.get_text():
                tble = i.find('table', {'class' : '_3ENrHu'})

        brand = d_data.find_all('div', {'class' : '_1HEvv0'})
        name = brand[-1].get_text().strip('\n')
        brand = brand[-2].get_text()
        #print(brand, name)

        dictionary = {
                        'name' : name,
                        'brand' : brand,
                        'image_no' : len(img),
                        'image_links' : img,
                        'ratings' : ratings,
                        'reviews_count' : reviews,
                        'price' : price
                     }

        json_list.append(dictionary)
        
    except Exception:
        pass

with open('flipcart_scraper_3.json', 'a') as f:
    json.dump(json_list, f, indent = 4)




