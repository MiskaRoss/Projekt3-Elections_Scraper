"""
projekt_3.py: t�et� projekt do Engeto Online Python Akademie
author: Michaela Rossmannov�
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
     Ov��en� zda je funk�n� odkaz a vr�t� kod strakny v html.
     Ze kter�ho se z�skat dal�� informace.
    '''
    response = requests.get(adresa_URL)
    soup = bea(response.text, 'html.parser')
    print(f'STAHUJI DATA z adresy: {adresa_URL}')
    return soup
def seznam_mest() -> list:
    '''
    Funkce:
    Vrat� list se seznamem jmen m�st z daneho odkazu funkce: odkaz_pro_stahovani()
    Tato funkce pro spravne fungovani pot�ebuje m�t vytvo�enou prom�nou: soup , v globalnim prostredi kodu,ve kter� je
    ulo�en odkazse kter�m pracuje a zisk�va zn�j data.
    '''
    mesta = []
    ziskani_mesta = soup.find_all('td','overflow_name')
    for mesto in ziskani_mesta:
        mesta.append(mesto.text)
    return mesta
def adresa_mest() -> list:
    '''
    Funkce n�m do listu ulo�� celou url adresu m�sta, ze kter� pak d�le stahovat informace.
    Tato funkce pro spravne fungovani pot�ebuje m�t vytvo�enou prom�nou: soup , v globalnim prostredi kodu , ve kter�
    je ulo�en odkaz se kter�m pracuje a zisk�va zn�j data.
    '''
    link_mesta = []
    ziskani_link_mesta = soup.find_all('td','cislo','href')
    for l in ziskani_link_mesta:
        l = l.a['href']
        link_mesta.append(f'https://volby.cz/pls/ps2017nss/{l}')
    return link_mesta
def id_mesta() -> list:
    '''
    Vr�ti ID �islo obce.
    Tato funkce pro spravne fungovani pot�ebuje m�t vytvo�enou prom�nou: soup , v globalnim prostredi kodu, ve kter� je
    ulo�en odkaz se kter�m pracuje a zisk�va zn�j data.
    '''
    id_mest = []
    id = soup.find_all('td','cislo')
    for i in id:
        id_mest.append(i.text)
    return id_mest
def politicke_strany() -> list:
    '''
    Vytvo�� list s n�szvem politickych stran pro zadane m�sta.
    Vystup:
     -v�stupem je list s nasvem politickys stran
     p�: ['ODS',......]
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
    Z�sk� celkov� po�et voli�u z m�st, kter� jsou ziskany z funkce => adresa_mest.
    Vystup:
     -v�stupem je list s hodnotami
     p�: ['8','9','3'......]
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
    Z�sk� celkov� po�et vydan�ch ob�lek z m�st, kter� jsou ziskany z funkce => adresa_mest.
    Vystup:
     -vystupem je list s hodnotami
     p�: ['8','9','3'......]
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
     Z�sk� celkov� po�et platn�ch hlas� z m�st, kter� jsou ziskany z funkce => adresa_mest.
     Vystup:
     -vystupem je list s hodnotami
     p�: ['8','9','3'......]
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
    Vytvo�� list kde jsou uvedeny po�ty hlasu dan� strany, pro kazde mesto, kter� n�m brat� funkce: adresa_mest().
     Vystup:
     -vystupem je list s hodnotami
     p�: ['8','9','3'......]
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
    Pomoci funkc�: volici_pocet,vydane_obalky, platne_hlasy, seznam_mest, id_mest, strany_pocet_hlasu , vytvo�� pro
    ka�d� mesto listk, ktery opsahuje ve�kere pozadovban� informace, kter� se nasledne daj� propsat do souboru typu csv.
    V�stup:
    - ['572560', 'Ban�n', '264', '157', '157', '7', '0', '0', '12'.......]
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
    Ta to funkce slou�i pro zapsan� dat do souboru typu .csv.
    Bere informace z funkc�ch: vstup_mesta, politick� stran a tyto data vlo�i do tabulek s nazvem souboru
    ,kter� zad�te do prametru funkce.
    '''
    sloupek = ['K�d obce', 'N�zev obce', 'Voli�i v seznamu', 'Vydan� ob�lky', 'Platn� hlasy']
    mesta = vystup_mesta()
    strany = politicke_strany()
    print(f'Ukld�m data do souboru: {nazev_souboru}')
    for party in strany:
        sloupek.append(party)
    with open(nazev_souboru,mode='w', newline='',encoding='utf-8') as soubor:
        soubor_writer = csv.writer(soubor)
        soubor_writer.writerow(sloupek)
        soubor_writer.writerows(mesta)
    print(f'Ukonc�uji: {sys.argv[0]}')


#### Ov�reni atributu a ziskani prom�n� soup
if len(sys.argv) == 3:
    soup = odkaz_pro_stahovani(sys.argv[1])
else:
    print('Zadal jsi nepsravn� po�et argumentu. Mus� zadat 3.')
    quit()


if __name__ == '__main__':
    webova_adresa = sys.argv[1]
    nazev_souboru = sys.argv[2]
    vysledky_voleb(nazev_souboru)