import pandas as pd
from pandas.io.html import read_html

page = "https://meta.wikimedia.org/wiki/BBC_100_Women_in_2019"
wikitables = read_html(page)
prima_colonna = wikitables[0]['Article'].str.split()
prima_colonna.to_excel("bday.xlsx")