import requests
import json
from bs4 import BeautifulSoup
import re


#response = requests.get('https://www.flipkart.com/boat-rockerz-255f-bluetooth-headset/p/itm4b5bc4473563b?pid=ACCF6SZ8EFWFEPZ6&lid=LSTACCF6SZ8EFWFEPZ6WFAW4Y&marketplace=FLIPKART&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_0_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_0_4_na_na_na&fm=SEARCH&iid=dec307b9-73fa-4b7f-a5ea-73fba4216faf.ACCF6SZ8EFWFEPZ6.SEARCH&ppt=sp&ppn=sp&ssid=f4oy78xtow0000001583342829051&qH=edd443896ef5dbfc')
response = requests.get('https://www.flipkart.com/realme-c3-frozen-blue-32-gb/p/itm58bf81a807d66?pid=MOBFZHC5HAGKGBBW&lid=LSTMOBFZHC5HAGKGBBWJH2HLH&marketplace=FLIPKART&srno=s_1_1&otracker=AS_Query_TrendingAutoSuggest_1_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_1_0_na_na_na&fm=SEARCH&iid=7ee341bd-a7d2-4320-803f-844d43fac2a9.MOBFZHC5HAGKGBBW.SEARCH&ppt=sp&ppn=sp&ssid=fw25kef5bk0000001583364588304&qH=eb4af0bf07c16429')

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
with open('flipcart.json', 'a') as f:
    json.dump(dictionary, f, indent = 4)

