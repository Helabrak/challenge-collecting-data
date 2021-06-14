from bs4 import BeautifulSoup
import requests
import time
import random
from random import randint
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from threading import Thread, RLock
import re

#setting up every variable, list, dictionary

list_of_links = []
navigation_links = []
general_info = []
page_number = 2
base_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page=1&orderBy=relevance"
driver = webdriver.Chrome("/Users/jacquesdeclercq/Desktop/BeCode Training/chromedriver")
driver.implicitly_wait(5)
driver.get(base_url)
time.sleep(random.uniform(1.0, 2.0))
lock = RLock()

# Open the URL, and click on the Keep Browsing button.

soup = BeautifulSoup(driver.page_source,'lxml')
cookies = driver.find_element_by_xpath('//*[@aria-label="Keep browsing"]')
cookies.click()

#Gets every link of every property on a page

def run_through_pages():
    while len(list_of_links) < 5:
        for links in soup.find_all('a',attrs={"class" :"card__title-link"}) :
            list_of_links.append(links.get("href"))

#Get the link(href) for the next page

def get_and_next_page():
        for navigation in soup.find_all('a', attrs={"class" : "pagination__link pagination__link--next button button--text button--size-small"}):
            navigation_links.append(navigation.get("href"))
            driver.get(navigation.get("href"))

#Opens the links scraped from the homepage

def open_links():
    for link in list_of_links:
        driver.get(link)

#Scrape code for number of bedrooms

def scrape_through():
    bedroom_list = []
    property_type_list = []
    type_of_sale_list = []
    property_price_list = []
    property_area_list = []
    soup = BeautifulSoup(driver.page_source,'lxml')


    general_info=soup.body.main.find('div',{'class': 'text-block'}).text
    for number_of_bedrooms in general_info:
        number_of_bedrooms=str.split(general_info)[1]
        print(bedroom_list.append(number_of_bedrooms))

    property=soup.body.main.find('h1',{'class': 'classified__title'}).text
    for type_of_property in property:
        type_of_property=str.split(property)[0]
        print(property_type_list.append(type_of_property))

    sale_property=soup.body.main.find('h1',{'class': 'classified__title'}).text
    for type_of_sale in sale_property:
        type_of_sale = str.split(sale_property)[2]
        print(type_of_sale_list.append(type_of_sale))

    property_price = soup.body.main.find('span',{'class': 'sr_only'}).text
    for prices in property_price:
        print(property_price_list.append(prices))

    property_area = soup.body.main.find('div',{'class': 'text-block'}).text
    for areas in property_area:
        areas = str.split(property_area)[5]
        print(property_area_list.append(areas))

#Bilal's Scrape

def scrape_through_pages():
    soup = BeautifulSoup(driver.page_source,'lxml')
    parameters = {}
    for match in soup.find_all( 'span' ):  # add these two extra two lines
        match.unwrap()
    for elem in soup.find_all( 'tr' ):
        td_elem = elem.find( 'th' )
        td2 = re.sub( "^<th class=\"classified-table__header\" scope=\"row\">|</th>$", "", str( td_elem ) )
        td3 = re.sub( "\\n *", "", td2 )
        td4 = re.sub( "<th class=\"classified-table__header\">", "", td3 )
        th_elem = elem.find( 'td' )
        th2 = re.sub( "^<td class=\"classified-table__data\">|</td>$", "", str( th_elem ) )
        th3 = re.sub( "\\n *", "", th2 )
        th4 = re.sub( "m² *square meters", "", th3 )
        th5 = re.sub( " <br/>", " ", th4 )
        parameters[td4] = th5
    return parameters

#Bilal's cleaning the scraped data

def clean_the_data():#parameters, soup
    parameters = {}
    all_parameters = []
    #adress = parameters["Address"].split()
    #all_parameters.append( adress[-1] )
    # type house
    type_of_property = soup.find( "h1", {"class": "classified__title"} )
    type_of_property = type_of_property.split()[0]
    all_parameters.append( type_of_property )
    # house or app
    if type_of_property == "Apartment":
        house_or_app = "Apartment"
    else:
        house_or_app = "House"
    all_parameters.append( house_or_app )
    # Price
    price = soup.find( "p", {"class": "classified__price"} )
    price = price.split()[1]
    price = re.sub( "€", "", price )
    all_parameters.append( price )
    # Type of sale (Exclusion of life sales)--------------------- not found
    all_parameters.append( "Exclusion" )
    # Number of rooms
    Number_of_rooms = parameters["Bedrooms"]
    all_parameters.append( Number_of_rooms )
    # Area
    Area = parameters["Living area"]
    all_parameters.append( Area )
    # Fully equipped kitchen (Yes/No)
    if parameters["Kitchen type"] == "Installed":
        kitchen = "Yes"
    else:
        kitchen = "No"
    all_parameters.append( kitchen )
    # Furnished (Yes/No)
    Furnished = parameters["Furnished"]
    all_parameters.append( Furnished )
    # Open fire (Yes/No)
    if "How many fireplaces?" in parameters:
        fireplaces = "Yes"
    else:
        fireplaces = "No"
    all_parameters.append( fireplaces )
    # Terrace (Yes/No) - If yes: Area
    if "Terrace surface" in parameters:
        terrace = "Yes"
        terrace_area = parameters["Terrace surface"]
    else:
        terrace = "No"
        terrace_area = 0
    all_parameters.append( terrace )
    all_parameters.append( terrace_area )
    # Garden (Yes/No) - If yes: Area
    if "Garden surface" in parameters:
        garden = "Yes"
        garden_area = parameters["Garden surface"]
    else:
        garden = "No"
        garden_area = 0
    all_parameters.append( garden )
    all_parameters.append( garden_area )
    # Surface of the land
    if "Surface of the plot" in parameters:
        area_land = parameters["Surface of the plot"]

    else:
        area_land = "No"
    all_parameters.append( area_land )
    # Surface area of the plot of land---------------------------- not found
    # area_plot = parameters["Surface of the plot"]
    all_parameters.append( "None" )
    # Number of facades
    facades = parameters["Number of frontages"]
    all_parameters.append( facades )
    # Swimming pool (Yes/No)
    if "Swimming pool" in parameters:
        pool = "Yes"
    else:
        pool = "No"
    all_parameters.append( pool )
    # State of the building (New, to be renovated, ...)
    state_building = parameters["Building condition"]
    all_parameters.append( state_building )
    return all_parameters


def write_to_csv():
    with open("ImmoEliza.csv", 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerows(list_of_links)
        writer.writerows(bedroom_list)
        writer.writerows(property_type_list)
        writer.writerows(type_of_sale_list)


run_through_pages()
get_and_next_page()
open_links()
scrape_through_leo()
#clean_the_data()


#with open("ImmoEliza.csv", 'w', encoding='UTF8') as file:
 #   writer = csv.writer(file)
  #  writer.writerows(list_of_links)


