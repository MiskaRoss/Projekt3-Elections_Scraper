# Engeto_Project_3

Engeto 3rd project - Elections scraper.

## Application description
The election sraper project is used to download a defined part and then sort data from the website of the statistical office on the portal www.volby.cz. You can choose any district for scraping and than name the resulting file according to your requirements but the file extension must be csv.

## Installation of libraries

The used libraries that are part of the project are located in the requirements.txt file. To be able to install the used libraries, create a virtual environment and install the necessary packages:

```
$ pip3 --version                   # Verify the manager's version
$ pip3 install -r requirements.txt # installing libraries
```

## Starting the program

To run the main.py file, you need 2  arguments.

python main.py <"url referring to the desired territory"> <"file_name.csv">

```
python main.py <url_of_the_territorial_unit> <output_file_name>
```


## Sample program (example)

Voting results for the Benešov district:

If you want to take result from Benešov district, in terminal (pycharm) you have to input link of this district and your own name of exported csv file, for example Benesov.csv. Or you can input any district you want and any name of exported file.

1. argument(URL): "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201"

2. argument(filename): "vysledky_kromeriz.csv"

```
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201" "vysledky_kromeriz.csv"
```

### Downloading

DOWNLOADING DATA FROM THE ADDRESS: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201
DOWNLOADING DATA FROM THE ADDRESS: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201
DOWNLOADING DATA FROM THE ADDRESS: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201
DOWNLOADING DATA FROM THE ADDRESS: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201

I save the data to a file: vysledky_kromeriz.csv

Download complete. Saved file: main.py


## Expected output

```
Town-code,Towm_name,Registered, Enveloped, Valid notes,...
588300,Bařice-Velké Těšany,374,269,268,...
588326,Bezměrov,426,270,264,...
542318,Blazice,172,120,120,...
549690,Bořenovice,149,100,99,...
588377,Brusné,301,197,196,...

```
