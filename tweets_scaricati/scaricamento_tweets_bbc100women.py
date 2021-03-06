# il seguente script viene eseguito per ogni singolo anno considerato (di seguito viene riportato lo script per l'anno 2015)

import csv
import time
import json
import twint
import os.path
import datetime
import nest_asyncio
import pandas as pd 
from datetime import datetime
from datetime import timedelta

# creo un nuovo dataset completo
complete_tweets_db = pd.DataFrame()

# impostazione date
nest_asyncio.apply() # Blocco eventuali loop di ricerca in corso

# Data inizio ricerca: la ricerca inizia dal giorno più recente
until = datetime(2015,12,31,00,00,00)
until = until + timedelta(days=1) # per considerare tutte le 24 ore del primo giorno
print("Until:    ", until)

# Data fine ricerca: scaricamento tweets fino a questo data (più vecchia) rimane fissa
since = datetime(2015,1,1,00,00,00)

# since = datetime(2015,1,1,00,00,00)
print("Since:    ", since)

# Questo since è il giorno che continua a cambiare
changing = until - timedelta(days=1) 
print("Changing: ", changing)

# conteggio giorni rimanenti
remaining_days = int(str(changing-since).split()[0])

# query BBC100World
user_mention = "@BBC100Women"
hashtags_considerati = "#BBC100Women OR #BBC100women OR #bbc100women OR #Bbc100Women OR #bbc100WOMEN OR #bBc100women OR #BBC100WOMEN"
query = "({} OR {})".format(user_mention, hashtags_considerati)
print(query)

##------------- Download dei tweets -------------## 
while True:
 
    print("-----------------------------------------------")
    print('\nDobbiamo scaricare fino al giorno: ', since.strftime('%Y-%m-%d'))
    print('\nStiamo scaricando i tweets del giorno: ', (until - timedelta(days=1)).strftime('%Y-%m-%d'))
    print('\nQuindi tutti quei tweets compresi nel seguente intervallo temporale:  {} <-------> {}'.format(changing, until))
    print('\nRimangono da scaricare {} giorni'.format(remaining_days))
    print("\nSTART COLLECTING...")
    
    c = twint.Config()
    c.Search = query
    c.Store_csv = True
    c.Since = changing.strftime('%Y-%m-%d %H:%M:%S') 
    c.Until = until.strftime('%Y-%m-%d %H:%M:%S')    
    c.Pandas=True
    c.Count=True
    c.Hide_output=True

    twint.run.Search(c)
    
    # Importo i dati giornalieri nel dataframe completo
    complete_tweets_db = complete_tweets_db.append(twint.storage.panda.Tweets_df)

    if int(str(changing-since)[0]) == 0: # significa che abbiamo considerati tutti i giorni del nostro arco temporale generale, quindi il ciclo di ricerca deve stopparsi
      break

    # Cambio finestra temporale a livello giornaliero  
    changing = changing - timedelta(days = 1) # sarebbe il since
    until = until - timedelta(days = 1)

    if str(changing-since).split()[0] == '0:00:00': # necessario per evitare errore stampa output ultimo giorno
      remaining_days = 0 
    else:
      remaining_days = int(str(changing-since).split()[0])

    nest_asyncio.apply() # resetto loop di ricerca cosi non sembra un attacco dos

    print('\n', end='\r')

complete_tweets_db.head()

complete_tweets_db.shape

# settiamo l'indice a 'id'
complete_tweets_db.set_index(keys='id', inplace=True)

# selezione dei campi utili
complete_tweets_db_new = complete_tweets_db[[ 'date', 'place', 'tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets', 'geo']]
complete_tweets_db_new.head()
# complete_tweets_db_new.shape

# individuazione duplicati
print(complete_tweets_db_new[complete_tweets_db_new.index.duplicated()])
# duplicateRowsDF = complete_tweets_db_new[complete_tweets_db_new.index.duplicated()]
# print("Duplicate Rows based on a single column are:", duplicateRowsDF, sep='\n')

# eliminazione dei duplicati
complete_tweets_db_new_no_duplicates = complete_tweets_db[~complete_tweets_db.index.duplicated()]
complete_tweets_db_new_no_duplicates.shape

# salvataggio in formato in csv
complete_tweets_db_new.to_csv("tweets_2015.csv")

# salvataggio tweets in formato json

with open('tweets_2015.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with open('tweets_2015.json', 'w') as f:
    json.dump(rows, f)