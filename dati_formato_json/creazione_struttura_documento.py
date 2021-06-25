# !pip install pymongo
# !pip install numpyencoder
# !pip install simplejson
import pandas as pd
# from pymongo import MongoClient
import json
import simplejson
import numpy
from numpyencoder import NumpyEncoder

# funzione
def costruzione_doc(year, dati_donne_indicatori_stato_anno):

  anno = year
  dati_donne_indicatori_stato_anno = dati_donne_indicatori_stato_anno

  elenco_donne = {
      "winning_women" : []
  }

  indicatori = {
      "indicators": []
  }

  document[anno] = []
  document[anno].append(elenco_donne)
  document[anno].append(indicatori)

  # inserisco i dati

  for row in dati_donne_indicatori_stato_anno.itertuples():
    donna_dati = {
            "id": row.id,
             "name": row.name,
             "image": row.image,
             "age": row.age,
             "category": row.category,
             "role": row.job,
             "description": row.description
             }
    indicatori_stato = {
              "gdp":row.gdp,
              "gdp_capita": row.gdp_pro_capita,
              "ratio_labour": row.labour_percentage,
              "gender_gap": row.gender_gap,
              "human_development": row.hdi
          }
    elenco_donne.get("winning_women").append(donna_dati)

    if indicatori.get("indicators") == []:
      indicatori.get("indicators").append(indicatori_stato)

csv_db= pd.read_csv('tabelle_finali_donne_indicatori_stati/tabella_finale_finale_V3.csv')
csv_groups= csv_db.groupby("country") # raggruppo per stato

documents = []

for country in csv_groups: # ciclo sui vari stati

  nome_stato = country[0] # nome dello stato considerato
  donne_indicatori_stato = country[1] # donne vincitrici dello stato in questione + indicatori stato

  document = {
      "country" : nome_stato
    }

  donne_indicatori_group_year = donne_indicatori_stato.groupby('year') # raggruppo per anno le donne vincitrici dello stato in questione
  
  for donne_indicatori_year in donne_indicatori_group_year: # considero le donne del 2015, le donne del 2020 per lo stato in questione

     anno = donne_indicatori_year[0] # anno considerato
     dati_donne_indicatori_stato_anno = donne_indicatori_year[1] # donne vincitrici dello stato in questione + indicatori stato per lo specifico anno e stato
     
     if anno == 2015:
      costruzione_doc("2015", dati_donne_indicatori_stato_anno) # inserisco dati per il 2015
     if anno == 2019:
       costruzione_doc("2019", dati_donne_indicatori_stato_anno) # inserisco dati per il 20219

  documents.append(document) # passo ad analizzare un nuovo stato

print(documents)

with open('countries_women.json', 'w') as f:
  simplejson.dump(documents, f, ignore_nan=True)
  # json.dump(documents, f, cls=NumpyEncoder)
