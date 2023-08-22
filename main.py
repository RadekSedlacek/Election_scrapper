"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Radek Sedláček
email: radek.sedlacek13@email.cz
discord: elvinek
"""

import requests
from bs4 import BeautifulSoup as bs
import sys
import csv

url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
response_base = requests.get(url)
soup_base = bs(response_base.text, features="html.parser")

def scrap_elections (place : str, output :str) -> csv:
    """
    This is the main function for district scraping.
    It uses other functions while creating it's own variables.
    """
    new_url = create_new_url (find_new_url (place))
    response_2 = requests.get(new_url)
    soup_2 = bs(response_2.text, features="html.parser")
    all_towns = soup_2.find_all("td", attrs={"class": "cislo"})
    final_urls = []
    for town in all_towns:
        a_element = town.find("a")
        href2 = a_element["href"]
        final_url = f"https://volby.cz/pls/ps2017nss/{href2}"
        final_urls.append(final_url)
    codes = get_codes(soup_2)
    locations = get_location (soup_2)
    rest = get_rest (final_urls)
    create_csv(codes, locations, rest, output)
    
def find_new_url (place: str) -> str:
    """
    This finds a relevant url part on the base website relevant to name of the district form user input.
    """
    tag_with_place = soup_base.find("td", string=place)
    if tag_with_place:
        tag_with_url = tag_with_place.find_next_sibling("td").find_next_sibling("td")
        tag_a = tag_with_url.find("a")
        url_part = tag_a["href"]
        return url_part
    else:
        print("District not found.")
        quit ()

def create_new_url (url_part: str) -> str:
    """
    This creates a new url form the base part of the url, that is always the same and adds to it, to create a new one.
    """
    new_url = f"https://volby.cz/pls/ps2017nss/{url_part}"
    return new_url

def get_codes (soup) -> list:
    """
    This part gets codes of the cities within district and returns a list of them.
    """
    codes_code = soup.find_all("td", {"class": "cislo"})
    codes = []
    for code in codes_code:
        a_element = code.find("a")
        displayed_text = a_element.text
        codes.append(displayed_text)
    return codes

def get_location (soup) -> list:
    """
    This part gets names of the cities within district and returns a list of them.
    """
    location_code = soup.find_all("td", {"class": "overflow_name"})
    locations = []
    for location in location_code:
        displayed_text = location.text
        locations.append(displayed_text)
    return locations

def get_rest(urls: list) -> list:
    """
    This part gets a list of parties from the firts city of the district and then it cycles throught every city and collects relevant data.
    It returns a list of parties, and lists containing rigistered voters, distributed envelopes, valid votes 
    and a list containing several list of votes for every party (every party has its own list in a list called "votes").
    It also cleanes the data, because numbers over 999 coontained "\xa0" between thousand and hundred digit.
    """
    registered = []
    envelopes = []
    valid = []
    parties = []
    
    response_parties = requests.get(urls[0])
    soup_parties = bs(response_parties.text, features="html.parser")
    parties_code = soup_parties.find_all("td", {"class": "overflow_name"})
    for party in parties_code:
        displayed_text = party.text
        parties.append(displayed_text)

    votes = [[] for party in parties]
        
    for url in urls:
        response_final = requests.get(url)
        soup_final = bs(response_final.text, features="html.parser")
        
        registered_code = soup_final.find("td", {"class": "cislo", "headers": "sa2"})
        displayed_text = registered_code.text
        registered.append(displayed_text)
        
        envelopes_code = soup_final.find("td", {"class": "cislo", "headers": "sa3"})
        displayed_text = envelopes_code.text
        envelopes.append(displayed_text)

        valid_code = soup_final.find("td", {"class": "cislo", "headers": "sa6"})
        displayed_text = valid_code.text
        valid.append(displayed_text)

        tags_with_party = soup_final.find_all("td", {"class": "overflow_name"})
        list_num = 0
        for tag in tags_with_party:
            tag_with_votes = tag.find_next_sibling("td")
            vote_text = tag_with_votes.text
            vote_text_clean = vote_text.replace("\xa0", " ")
            votes[list_num].append(vote_text_clean)
            list_num +=1
  
    registered_clean = [string.replace("\xa0", " ") for string in registered]
    envelopes_clean = [string.replace("\xa0", " ") for string in envelopes]
    valid_clean = [string.replace("\xa0", " ") for string in valid]
    
    return registered_clean, envelopes_clean, valid_clean, parties, votes

def create_csv (codes: list, locations: list, rest: list, file: str) -> csv:
    """
    This creates a .csv file called by user input, containing all the scraped data, for every town, in this format:
    code     |location |registered       |envelopes                 |valid           |party1      |party2      |party3      |
    town code|town name| # of reg. voters|# of envelopes distributed|# of valid votes|votes for p1|votes for p2|votes for p3|
    """
    parties = rest[3]
    header = ["code", "location", "registered", "envelopes", "valid"] + parties
    with open (file, mode ="w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(header)
        count = 0
        for count in range(len(codes)):
            row = [codes[count], locations[count], rest[0][count], rest[1][count], rest[2][count]] + [rest[4][party_idx][count] for party_idx in range (len(parties))]
            writer.writerow(row)
            count += 1

def scrap_zahranici (output: str) -> csv:
    """
    This is a main code for crapping "Zahraničí", because the procces is a little different form other districts you can scrap.
    Most of the functions this uses are adjusted specifically, and are made into their own functions. I find it a little clearer than branchning out functions above.
    """
    response = requests.get("https://volby.cz/pls/ps2017nss/ps36?xjazyk=CZ")
    soup = bs(response.text, features="html.parser")
    locations = get_location_zahranici(soup)
    all_cities = soup.find_all("td", attrs={"class": "cislo"})
    final_urls = []
    for city in all_cities: 
        a_element = city.find("a")
        href = a_element["href"]
        final_url = f"https://volby.cz/pls/ps2017nss/{href}"
        final_urls.append(final_url)
    rest = get_rest (final_urls)
    create_csv_zahranici(locations, rest, output)

def get_location_zahranici(soup) -> list:
    """
    This part gets names of the cities abroad and returns a list of them.
    """
    location_code = soup.find_all("td", {"headers": "s3"})
    locations = []
    for location in location_code:
        displayed_text = location.text
        locations.append(displayed_text)
    return locations

def create_csv_zahranici (locations: list, rest: list, file: str) -> csv:
    """
    This creates a .csv file called by user input, containing all the scraped data, for every town, in this format:
    location |registered       |envelopes                 |valid           |party1      |party2      |party3      |
    city name| # of reg. voters|# of envelopes distributed|# of valid votes|votes for p1|votes for p2|votes for p3|
    """
    parties = rest[3]
    header = ["location", "registered", "envelopes", "valid"] + parties
    with open (file, mode ="w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(header)
        count = 0
        for count in range(len(locations)):
            row = [ locations[count], rest[0][count], rest[1][count], rest[2][count]] + [rest[4][party_idx][count] for party_idx in range (len(parties))]
            writer.writerow(row)
            count += 1

if len (sys.argv)  != 3:
    print ("Please, enter two arguments.")
elif ".csv" != sys.argv[2][-4:]:
    print ("Second argument has to be a name of .csv file, including \".csv\" at the end of it.")
elif sys.argv[1] == "Zahraničí":
    print (f"Scraping election data for Zahraničí and saving them into {sys.argv[2]}...")
    scrap_zahranici (sys.argv[2])
    print ("Done!")
else:
    print (f"Scraping election data for {sys.argv[1]} and saving them into {sys.argv[2]}...")
    scrap_elections (sys.argv[1], sys.argv[2])
    print ("Done!")
