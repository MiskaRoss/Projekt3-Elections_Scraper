"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Michaela Rossmannová
email: rossmannova.m@gmail.com
discord: misa02907
"""

import csv
import sys
import requests
from bs4 import BeautifulSoup


# Odkaz pro stahování:
def get_url():
    base_url = sys.argv[1]
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f'DOWNLOADING DATA FROM THE ADDRESS: {base_url}')
    return soup


# získá číselné označení obcí
def get_town_numbers() -> list:
    town_numbers = []
    code_elements = get_url().find_all("td", "cislo")
    for c in code_elements:
        town_numbers.append(c.text)
    return town_numbers


# Získá názvy obcí
def get_town_names() -> list:
    town_names = []
    town_elements = get_url().find_all("td", "overflow_name")
    for t in town_elements:
        town_names.append(t.text)
    return town_names


# vytvoří list s jednotlivými url obcí
def get_town_url() -> list:
    url_list = []
    url_town = get_url().find_all("td", "cislo", "href")
    for ul in url_town:
        ul = ul.a["href"]
        url_list.append(f'https://volby.cz/pls/ps2017nss/{ul}')
    return url_list


# získá počet voličů v seznamu
def get_registered() -> list:
    register_list = []
    cities = get_town_url()
    for link in cities:
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        people = soup.find_all('td', headers='sa2')
        for r in people:
            register_list.append(r.text)
    return register_list


# vydané obálky:
def get_envelopes():
    envelope_list = []
    cities = get_town_url()
    for link in cities:
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        people = soup.find_all('td', headers='sa3')
        for e in people:
            envelope_list.append(e.text)
    return envelope_list


# získá počet platných hlasů
def get_valid_votes() -> list:
    validate_list = []
    cities = get_town_url()
    for link in cities:
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        people = soup.find_all('td', headers='sa6')
        for p in people:
            validate_list.append(p.text)
    return validate_list


# získá názvy všech stran
def get_party() -> list:
    parties = []
    cities = get_town_url()
    response = requests.get(cities[0])
    soup = BeautifulSoup(response.text, "html.parser")
    url_parties = soup.find_all("td", "overflow_name")
    for c in url_parties:
        parties.append(c.text)
    return parties


# vytvoří list se všemi hlasy v dané obci
def get_votes() -> list:
    votes_list = []
    cities = get_town_url()
    for link in cities:
        html = requests.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        votes_of_parties = soup.find_all('td', 'cislo', headers=["t1sb3", 't2sb3'])
        votes = []
        for v in votes_of_parties:
            votes.append(v.text)
        votes_list.append(votes)
    return votes_list


# vytvoří se soubor dle druhého zadaného argumentu a vypíše se tabulka řádek po řádku
def output_town() -> list:
    rows = []
    town_codes = get_town_numbers()
    town_names = get_town_names()
    registered = get_registered()
    envelopes = get_envelopes()
    valid_votes = get_valid_votes()
    get_parties = get_votes()

    zipped = zip(town_codes, town_names, registered, envelopes, valid_votes)
    information_town = []
    for c, t, r, e, v in zipped:
        information_town.append([c, t, r, e, v])
    zip_all = zip(information_town, get_parties)
    for it, gp in zip_all:
        rows.append(it + gp)
    return rows


def output_election_results(name_of_file):
    column = ["Town_code", "Town_name", "Registered", "Envelopes", "Valid Votes"]
    towns = output_town()
    parties = get_party()
    print(f"I save the data to a file: {name_of_file}")
    for party in parties:
        column.append(party)

    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(column)
        file_writer.writerows(towns)
    print(f"Download complete. Saved file: {sys.argv[0]}")


def check_arguments():
    if len(sys.argv) != 3:
        print("Program need 2 arguments, I'm exiting the program")
        exit()
    elif not sys.argv[2].endswith(".csv"):
        print("Must be .csv file, I'm exiting the program")
        exit()


if __name__ == "__main__":
    check_arguments()
    url = sys.argv[1]
    file_name = sys.argv[2]
    output_election_results(file_name)
