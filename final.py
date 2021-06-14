from bs4 import BeautifulSoup
import requests
import pandas as pd

source=requests.get('https://www.immoweb.be/en/classified/apartment/for-sale/bertrix/6880/9376985?searchId=60c31d9d837ba').text
soup = BeautifulSoup(source,'lxml')

'''the levels:
#html
    #head(this one we dont need)
    body
        div id= "main-container" class="main-container"
            div id= "container-main-content" class="container-main-content"
                div class="classified"
                    div id="classified-app"
                     main id="main-content" class="main"'''
        #here we start the header (under main):
                        # div id="classified-header-container" class="classified__header-container"- from it we get the property type-sale type and price -and wasnt able to get the locality)
main_header = soup.body.main.find( "div", {'id': 'classified-header-container'} )
#classified_header=main_header.find("div",{'id': 'classified-header'})- also this and the ones below could be added but gives errors
#classified_header2=classified_header.find("div",{'class': 'container-classified--header'})
property=soup.body.main.find('h1',{'class': 'classified__title'}).text
property_type=str.split(property)[0]
print(property_type)

property=soup.body.main.find('h1',{'class': 'classified__title'}).text
type_of_sale=str.split(property)[2]
print(type_of_sale)

price = soup.body.main.find( 'span', {'class': 'sr-only'} ).text
print(price)

locality=soup.body.find('span',{'class':'classified__information--address-row'})
print(locality)
locality_1=locality.span
print(locality_1)





''''grid=classified_header2.find("div",{'class': 'grid'})
grid_desktop=grid.find("div",{'class': 'grid__item desktop--9'})
primary_info=grid_desktop.find("div",{'class': 'classified__header-primary-info'})
#note sometimes it gives the error that a variable doesnt have a find attribute because we havent yet reached the detailed variable so continue normally'''

'''locality=soup.body.find('span',{'class':'city-line pl-4'})
print(locality)



general_section= soup.body.main.find('tbody',{'class':'classified-table__body'}).text
print(general_section)
locality=general_section.find('th',{'scope':'row'})
print(locality)'''