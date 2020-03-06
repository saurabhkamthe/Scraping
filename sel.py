from selenium import webdriver

driver=webdriver.Chrome()
driver.get('https://www.flipkart.com/')

s = driver.find_element_by_name('q')
s.send_keys('mobile')
s.submit()

import requests
import json
from bs4 import BeautifulSoup
import re

response = requests.get(driver.current_url)
#print(response.content)

r_data = BeautifulSoup(response.content, 'lxml')

#print(r_data)

d_data = r_data.find_all('div', {'class' : '_3liAhj'})
#print(len(d_data))

a_data = r_data.find_all('a', {'class' : '_2cLu-l'})
#print(len(a_data))

links_list = []
for i in d_data:
    name = i.find('a', {'class' : '_2cLu-l'})
    link = name.get('href')
    links_list.append(link)

json_list = []
for link in links_list:
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
    
with open('flipcart_scraped.json', 'a') as f:
    json.dump(json_list, f, indent = 4)

