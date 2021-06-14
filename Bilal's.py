from bs4 import BeautifulSoup
from os import path
import requests
import csv
import re
import time


def soup_link(link):
    url = link
    r = requests.get( url )
    # soup = BeautifulSoup(r.content,'lxml')
    return BeautifulSoup( r.text, "lxml" )


def get_some_par(soup):
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


def clean_param(parameters, soup):
    # parameters
    all_parameters = []
    adress = parameters["Address"].split()
    all_parameters.append( adress[-1] )
    # type house
    type_of_property = soup.find( "h1", {"class": "classified__title"} ).text
    type_of_property = type_of_property.split()[0]
    all_parameters.append( type_of_property )
    # house or app
    if type_of_property == "Apartment":
        house_or_app = "Apartment"
    else:
        house_or_app = "House"
    all_parameters.append( house_or_app )
    # Price
    price = soup.find( "p", {"class": "classified__price"} ).text
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


def data_to_csv(all_parameters):
    with open( "./letsdo.csv", "a+" ) as file:
        write = csv.writer( file )
        write.writerow( all_parameters )


if __name__ == '__main__':
    i = time.time()
    with open( "./letsdo.csv", "w" ) as fichier:
        fields = ['Locality', 'Type of property', 'Subtype of property', 'Price', 'Type of sale', 'Number of rooms',
                  'Area', 'Fully equipped kitchen', 'Furnished', 'Open fire', 'Terrace', 'Terrace Area', 'Garden',
                  'Garden Area', 'Surface of the land', 'Surface area of the plot of land', 'Number of facades',
                  'Swimming pool', 'State of the building']
        write = csv.writer( fichier )
        write.writerow( fields )
    # test link list

    link_list = ["https://www.immoweb.be/en/classified/house/for-sale/eeklo/9900/9356868?searchId=60c1d67834b77",
                 "https://www.immoweb.be/en/classified/apartment/for-sale/uccle/1180/9377260?searchId=60c351320eaf8",
                 "https://www.immoweb.be/en/classified/house/for-sale/modave/4577/9101952?searchId=60c71431b5f60"]

    for link in link_list:
        soup = soup_link( link )
        parameters = get_some_par( soup )
        print( parameters )
        all_parameters = clean_param( parameters, soup )
        data_to_csv( all_parameters )
    print( time.time() - i )