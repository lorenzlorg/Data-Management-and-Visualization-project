from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.bbc.com/news/world-50042279")
soup = BeautifulSoup(page.content, 'html.parser')

# Due esempi: trova il testo del titolo e il body della pagina
title = soup.title.text # gets you the text of the <title>(...)</title>
page_body = soup.body

# Stampa in formato html il codice della pagina
print(soup.prettify())

# Cerca tutti i nomi delle 100 donne
l_name = []
for item in soup.find_all("h4"):
  l_name.append(item.text)
  # print(item.contents)
  # print(item.text)

print(l_name)

# trova tutte le immagini a partire dalla prima (non considerando il banner iniziale)
l_image = []
for item in soup.find_all('img')[1:]:
      l_image.append(item['src'])

print(l_image)

# Rimuovi gli spazi bianchi che vengono ottenuti nella precedente lista
for elem in l_image:
  if elem == '':
    l_image.remove(elem)

print(l_image)

# Stampami tutti i valori di lista
for elem in l_image:
  print(elem)

# cerca i tag "span" e prendi il contenuto dell'attributo "class" e inseriscilo
# in lista per poi stamparla
l_class = []
for item in soup.find_all("span", attrs={"class":"card__header__strapline__location"}):
  l_class.append(item.text)
  # print(item.contents)
  # print(item.text)

print(l_class)

# Stora nella variabile country e role gli elementi specifici
country = []
role = []

for elem in l_class[0:len(l_class)-1:2]:
  country.append(elem)

for elem in l_class[1:len(l_class):2]:
  role.append(elem)

print(country)
print(role)

# Stampami tutti gli elementi "country"
for elem in country:
  print(elem)

# Stampami tutti gli elementi "role"
for elem in role:
  print(elem)

# Trova tutti i "li" item del body dal 48esimo in avanti(da Precious Adams in avanti)
all_li = page_body.find_all("li")[48:]

# Ritorna solo il primo risultato
all_li[2]

# Prova a cercare tutte gli alias di "instagram" o "twitter"
soup.find_all(name="span", attrs={"class":["card__header__strapline__instagram", "card__header__strapline__twitter"]})

# cerca i tag "span" e prendi il contenuto dell'attributo "class" e inseriscilo
# in lista per poi stamparla
find_insta_twitter = soup.find_all(name="span", class_ = ["card__header__strapline__instagram", "card__header__strapline__twitter"])
l_class_insta_twitter = []

for item in find_insta_twitter:
    l_class_insta_twitter.append(item.text)

print(l_class_insta_twitter)

for elem in l_class_insta_twitter:
  print(elem)

# Trova la categoria e storala in una variabile
description_find = soup.find_all(name="p", class_ = ["first_paragraph"])
description = []

for l in description_find:
    description.append(l.text)

print(description)

for l in description:
  print(l)

category = []
for l in soup.find_all('article')[1:]:
  category.append(l.get('class'))

print(category)

# Rimuoviamo tutti i "card" che non sono necessari
for elem in category:
  elem.remove(elem[0])

# La lista precedente vuole essere convertita in una lista di stringhe, facilmente maneggevoli
l_category = []
for elem in category:
  for inner in elem:
    elem = inner
    l_category.append(elem)

print(l_category)

for stringa in range(0, len(l_category)):
  l_category[stringa] = l_category[stringa][10:]

for elem in l_category:
  print(elem)

# Crea un dataframe che contenga tutte le colonne inerenti i vari elementi ottenuti
import pandas as pd
df = pd.DataFrame(zip(l_name, l_image, l_category, country, role, description),
                  columns =['name', 'image', 'category', 'Country', 'role', 'description'])
df

# index = False serve a specificare a pandas che non ci interessa avere l'indice nel file
# finale in csv
df.to_csv("BBC100Women_2019_original.csv", index=False, encoding='UTF-8')

