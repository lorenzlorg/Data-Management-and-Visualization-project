import requests
import pandas as pd

base_site = 'https://reports.weforum.org/global-gender-gap-report-2015/rankings/'

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)[0]

tables

output = tables.to_csv("dati_donne_indicatori_stati/global gender gap 2015/gender_gap_2015_original.csv", index=False)