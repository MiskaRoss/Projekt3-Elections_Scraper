"""
projekt_3.py: tøetí projekt do Engeto Online Python Akademie
author: Michaela Rossmannová
email: rossmannova.m@gmail.com
discord: misa02907
"""

import sys
import csv
from bs4 import BeautifulSoup as bea
import requests

def odkaz_pro_stahovani(adresa_URL):
    '''
    Funkce:
     Ovìøení zda je funkèní odkaz a vrátí kod strakny v html.
     Ze kterého se získat další informace.
    '''
    response = requests.get(adresa_URL)
    soup = bea(response.text, 'html.parser')
    print(f'STAHUJI DATA z adresy: {adresa_URL}')
    return soup
def seznam_mest() -> list:
    '''
    Funkce:
    Vratí list se seznamem jmen mìst z daneho odkazu funkce: odkaz_pro_stahovani()
    Tato funkce pro spravne fungovani potøebuje mít vytvoøenou promìnou: soup , v globalnim prostredi kodu,ve které je
    uložen odkazse kterým pracuje a ziskáva znìj data.
    '''
    mesta = []
    ziskani_mesta = soup.find_all('td','overflow_name')
    for mesto in ziskani_mesta:
        mesta.append(mesto.text)
    return mesta
def adresa_mest() -> list:
    '''
    Funkce nám do listu uloží celou url adresu mìsta, ze které pak dále stahovat informace.
    Tato funkce pro spravne fungovani potøebuje mít vytvoøenou promìnou: soup , v globalnim prostredi kodu , ve které
    je uložen odkaz se kterým pracuje a ziskáva znìj data.
    '''
    link_mesta = []
    ziskani_link_mesta = soup.find_all('td','cislo','href')
    for l in ziskani_link_mesta:
        l = l.a['href']
        link_mesta.append(f'https://volby.cz/pls/ps2017nss/{l}')
    return link_mesta
def id_mesta() -> list:
    '''
    Vráti ID èislo obce.
    Tato funkce pro spravne fungovani potøebuje mít vytvoøenou promìnou: soup , v globalnim prostredi kodu, ve které je
    uložen odkaz se kterým pracuje a ziskáva znìj data.
    '''
    id_mest = []
    id = soup.find_all('td','cislo')
    for i in id:
        id_mest.append(i.text)
    return id_mest
def politicke_strany() -> list:
    '''
    Vytvoøí list s nászvem politickych stran pro zadane mìsta.
    Vystup:
     -výstupem je list s nasvem politickys stran
     pø: ['ODS',......]
    '''
    strany = []
    mesta = adresa_mest()
    repsonse = requests.get(mesta[0])
    soup = bea(repsonse.text,'html.parser')
    link_strany = soup.find_all('td', 'overflow_name')
    for s in link_strany:
        strany.append(s.text)
    return strany
def volici_pocet() -> list:
    '''
    Získá celkový poèet volièu z mìst, které jsou ziskany z funkce => adresa_mest.
    Vystup:
     -výstupem je list s hodnotami
     pø: ['8','9','3'......]
    '''
    volici = []
    mesta = adresa_mest()
    for link in mesta:
        html = requests.get(link)
        soup = bea(html.text, 'html.parser')
        lide = soup.find_all('td', headers='sa2')
        for v in lide:
            volici.append(v.text)
    return volici

def vydane_obalky() -> list:
    '''
    Získá celkový poèet vydaných obálek z mìst, které jsou ziskany z funkce => adresa_mest.
    Vystup:
     -vystupem je list s hodnotami
     pø: ['8','9','3'......]
     '''
    ucast = []
    mesta = adresa_mest()
    for link in mesta:
        html = requests.get(link)
        soup = bea(html.text, 'html.parser')
        lide = soup.find_all('td', headers='sa3')
        for u in lide:
            ucast.append(u.text)
    return ucast

def platne_hlasy() -> list:
    '''
     Získá celkový poèet platných hlasù z mìst, které jsou ziskany z funkce => adresa_mest.
     Vystup:
     -vystupem je list s hodnotami
     pø: ['8','9','3'......]
     '''
    corect = []
    addres = adresa_mest()
    for link in addres:
        html = requests.get(link)
        soup = bea(html.text, 'html.parser')
        lide = soup.find_all('td', headers='sa6')
        for p in lide:
            corect.append(p.text)
    return corect

def strany_pocet_hlasu() -> list:
    '''
    Vytvoøí list kde jsou uvedeny poèty hlasu dané strany, pro kazde mesto, které nám bratí funkce: adresa_mest().
     Vystup:
     -vystupem je list s hodnotami
     pø: ['8','9','3'......]
    '''
    mesta = adresa_mest()
    volici = []
    for link in mesta:
        html = requests.get(link)
        soup = bea(html.text, 'html.parser')
        strany_hlasy = soup.find_all('td','cislo',headers=["t1sb3",'t2sb3'])
        hlasy= []
        for p in strany_hlasy:
            hlasy.append(p.text)
        volici.append(hlasy)
    return volici

def vystup_mesta() -> list:
    '''
    Pomoci funkcí: volici_pocet,vydane_obalky, platne_hlasy, seznam_mest, id_mest, strany_pocet_hlasu , vytvoøí pro
    každé mesto listk, ktery opsahuje veškere pozadovbané informace, které se nasledne dají propsat do souboru typu csv.
    Výstup:
    - ['572560', 'Banín', '264', '157', '157', '7', '0', '0', '12'.......]
    '''
    radek_mesta = []
    volic = volici_pocet()
    obalka = vydane_obalky()
    platny_hlas = platne_hlasy()
    mesta = seznam_mest()
    ids = id_mesta()
    volici_stran = strany_pocet_hlasu()
    zipped = zip(ids, mesta, volic, obalka, platny_hlas)
    info_mesto = []
    for i, m, v, o, p in zipped:
        info_mesto.append([i,m,v,o,p])
    zip_all = zip(info_mesto,volici_stran)
    for im,vs in zip_all:
        radek_mesta.append(im+vs)
    return radek_mesta

def vysledky_voleb(nazev_souboru):
    '''
    Ta to funkce slouži pro zapsaní dat do souboru typu .csv.
    Bere informace z funkcích: vstup_mesta, politické stran a tyto data vloži do tabulek s nazvem souboru
    ,které zadáte do prametru funkce.
    '''
    sloupek = ['Kód obce', 'Název obce', 'Volièi v seznamu', 'Vydané obálky', 'Platné hlasy']
    mesta = vystup_mesta()
    strany = politicke_strany()
    print(f'Ukldám data do souboru: {nazev_souboru}')
    for party in strany:
        sloupek.append(party)
    with open(nazev_souboru,mode='w', newline='',encoding='utf-8') as soubor:
        soubor_writer = csv.writer(soubor)
        soubor_writer.writerow(sloupek)
        soubor_writer.writerows(mesta)
    print(f'Ukoncèuji: {sys.argv[0]}')


#### Ovìreni atributu a ziskani promìné soup
if len(sys.argv) == 3:
    soup = odkaz_pro_stahovani(sys.argv[1])
else:
    print('Zadal jsi nepsravný poèet argumentu. Musíš zadat 3.')
    quit()


if __name__ == '__main__':
    webova_adresa = sys.argv[1]
    nazev_souboru = sys.argv[2]
    vysledky_voleb(nazev_souboru)