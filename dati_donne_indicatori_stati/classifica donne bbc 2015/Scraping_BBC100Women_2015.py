import re
import pandas as pd
import csv
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq  # urllib ci cattura quanto richiesto dall'HTML (è il nostro client)

my_url = 'https://www.bbc.co.uk/news/special/2015/newsspec_12497/content/english/index.html?v=0.1.24&hostid=www.bbc.com&hostUrl=https%3A%2F%2Fwww.bbc.com%2Fnews%2Fworld-34745739&iframeUID=responsive-iframe-61225031&onbbcdomain=true#facewall_15'

# Apre la connessione col sito, ottiene la pagina e la scarica
uClient = uReq(my_url)

# Ne leggo il contenuto e lo storo in una variabile
page_html = uClient.read()

# Chiudo la connessione col sito dopo aver letto la pagina
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# Prendi tutti i profili che variano con l'attributo "facewall_\d+" da 1 a 100 usando la regex
containers = page_soup.find_all("li", {"id": re.compile(r"facewall_\d+")})

# Controlla la lunghezza del file
len(containers)

with open("tabella_donne_2015.csv", "w", newline = "") as csv_file:
    # Create a writer
    writer = csv.writer(csv_file)
    # Create a header row
    writer.writerow(["name", "age", "job", "nationality", "description", "\n"])    

for container in containers:    
    # Trova il nome
    name = container.h2.text
    
    various = container.find_all("div", {"class": "facewall_profile_attribute"})
    
    # Trova l'età
    age = various[0].text[5:].strip()

    # Trova il lavoro
    job = various[1].text[5:].strip()
    
    # Trova la nazionalità
    nationality = various[2].text[13:].strip()
    
    # Trova la descrizione e unisci i vari paragrafi
    parag = container.find_all("p", {"class": "facewall_profile_paragraph"})
    
    full_string = ""
    for j in range(len(parag)):
        full_string += parag[j].text + " "
    full_string = full_string.strip()
    
    with open("BBC100Women_2015_original.csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, age, job, nationality, full_string, "\n"])

# conversione in formato xlsx
read_file = pd.read_csv (r'BBC100Women_2015_original.csv')
read_file.to_excel (r'BBC100Women_2015_original.xlsx', index = None, header=True)

"""
Manualmente siamo andati ad apportare modifiche direttamente sul file excel generato (BBC100Women_2015_original.xlsx). Alcune modifche quali:
    - da nazionalità a stato
    - corretta la sintassi di alcuni nomi
"""