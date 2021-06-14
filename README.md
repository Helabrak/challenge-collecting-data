ImmoEliza real-estate project request: 


Description: The client, "ImmoEliza" wants to create a machine learning model to make price predictions on real estate sales in Belgium. for that we worked on a dataset that provides information on 10,000 properties from one of the main real-estate websites for property search in Belgium, that is called Immoweb, the information on these properties covered the main search categories/parameters as listed below: 
  •	Locality
  •	Type of property (House/apartment)
  •	Subtype of property (Bungalow, Chalet, Mansion, ...)
  •	Price
  •	Type of sale (Exclusion of life sales)
  •	Number of rooms
  •	Area
  •	Fully equipped kitchen (Yes/No)
  •	Furnished (Yes/No)
  •	Open fire (Yes/No)
  •	Terrace (Yes/No)
  o	If yes: Area
  •	Garden (Yes/No)
  o	If yes: Area
  •	Surface of the land
  •	Surface area of the plot of land
  •	Number of facades
  •	Swimming pool (Yes/No)
  •	State of the building (New, to be renovated, ...)

Installation:
Both Beautifulsoup and Selenium were installed 

Usage:
from bs4 import BeautifulSoup
import requests

source=requests.get('https://www.immoweb.be/fr/annonce/appartement/a-vendre/mons/7000/9379673?searchId=60c4debf72b3c').text
soup = BeautifulSoup(source,'lxml')
print(soup.prettify())
main_container=soup.body.find("main",{'id': 'main-content'})
print(main_container.prettify())

property=soup.body.main.find('h1',{'class': 'classified__title'}).text
property_type=str.split(property)[0]
print(property_type)

property=soup.body.main.find('h1',{'class': 'classified__title'}).text
type_of_sale=str.split(property)[2]
print(type_of_sale)

price = soup.body.main.find( 'span', {'class': 'sr-only'} ).text
print(price)

Visuals:
None

Contributors:
other team members who worked on/contributed to this project:
Leonor Drummond:https://github.com/ltadrummond
JacquesDeclercq: https://github.com/JacquesDeclercq
Bilal Mesmoudi:https://github.com/BMesm


Data scraping: 
we used Beautiful soup to get the data from individul links for properties and then used selenium to automate the scraping for the same parameters across the website

Timeline: 
Project started june 10,2021 
Deadline to submit final presentation to the client: Monday 14/6/2021

personal situation:
This project was carried out to create a dataset that will build the foundation for a machine learning model to make price predictions on real estate sales in Belgium for ImmoEliza real-estate

