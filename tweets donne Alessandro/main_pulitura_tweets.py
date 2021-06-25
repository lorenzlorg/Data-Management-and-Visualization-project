import csv
import json
import simplejson
import pandas as pd

# apro il file
with open('tweets_donne_scaricati.json', 'r') as dataFile:
    data_json_finale = json.load(dataFile)

# ne creo una copia per evitare di pasticciare su quello caricato
copia_json = data_json_finale.copy()

# per ogni elemento presente, elimina il campo tweets se esiste (possibili
# anche toglierlo esistendo sempre nel nostro caso)
for element in copia_json:
    if 'tweets' in element:
        del element['tweets']

# salvataggio risultati
with open('final_output_pulito.json', 'w', encoding="UTF-8") as f:
    simplejson.dump(copia_json, f, ignore_nan=True)

# Riapro il file salvato
with open('final_output_pulito.json') as json_file:
    data_da_convertire = json.load(json_file)

# creo un oggetto e lo esporto in csv
pdObj = pd.read_json('final_output_pulito.json')
export_csv = pdObj.to_csv (r'tweets_donne_scaricati_viz.csv', header=True)

pdObj.to_csv(index=False)