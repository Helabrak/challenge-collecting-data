from bs4 import BeautifulSoup
import requests
import time
import random
from random import randint

from bs4 import BeautifulSoup
import requests
url = 'https://www.immoweb.be/en/classified/apartment/for-sale/tisselt/2830/9380215'
time.sleep(random.uniform(1.0, 2.0))
source = requests.get('https://www.immoweb.be/en/classified/apartment/for-sale/tisselt/2830/9380215').text
soup = BeautifulSoup(source,'lxml')
soup

#Let's get the basic elements - pretty clean
for overview in soup.find_all(class_="overview__text"):
        print(overview.get_text())

print("_________________________"*5)


#Let's get the porperty type - preaty clean
for type_property in soup.find_all(class_="classified__title"):
        print(type_property.get_text())

#Let's get the price - pretty clean
price = soup.find(class_="classified__price")
print(price.get_text())


print("_________________________"*5)

#let's get the content of the "General" information. I can print cleaner, but still not scrapped enought... Need some help here.
information_general_list = soup.find(class_="classified-table")
information_general_list_details = information_general_list.find_all("tr")

for information in information_general_list_details:
        print(information)


results = soup.find(class_="classified")
print(results)

print("============================="*50)

#ehere I can print the hole page, and aaaaall the elements from the house. However, I can not access them yet
house_elements = results.find_all("div", class_="text-block")

for elem in house_elements:
    print(elem)

#for elem in soup.find_all('div',attrs={"class" : "overview__text"}):
#        print(elem)
