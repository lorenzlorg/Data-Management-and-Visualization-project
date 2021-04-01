import csv
import time
import json
import twint
import os.path
import datetime
import simplejson
import nest_asyncio
import pandas as pd
from datetime import datetime
from datetime import timedelta
from jsonmerge import merge


def scaricamento_tweets(until, since, changing, remaining_days, complete_tweets_db, query):

    while True:
        time.sleep(1)
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
        c.Pandas= True
        c.Count= True
        c.Hide_output= True
        c.User_full= True

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

        # eliminazione dei duplicati
        complete_tweets_db_new_no_duplicates = complete_tweets_db[~complete_tweets_db.index.duplicated()]

    return complete_tweets_db_new_no_duplicates


# lista donne bbc
df_lista_donne = pd.read_csv("LOL.csv", sep=',')
df_lista_ridotta = df_lista_donne[["id", "name", "username_twitter", "hashtag", "year"]]

# creazione struttura json da riempire con i tweets pre e post classifica
donne_dictionary = {}

# la chiave sarà l'id della donna
for donna in df_lista_ridotta.itertuples():
  if donna[1] not in donne_dictionary:

    donne_dictionary[donna[1]] = {
        "tweets": {
            "pre-classifica": [],
            "post-classifica": []
        }
    }

    # {
    #     donne_dictionary[donna[1]] = {
    #     "tweets": {
    #         "pre-classifica": [],
    #         "number tweets pre-classifica "
    #         "post-classifica": []
    #         "number tweets pre-classifica "
    #     }
    #     nome: nome_donna
    #
    # }


# Download dei tweets
for riga in df_lista_ridotta.itertuples():

    print("\n\n" + "*"*50 + riga.name + "*"*50)

    complete_tweets_db = pd.DataFrame()  # creo un nuovo dataset completo
    nest_asyncio.apply()  # Blocco eventuali loop di ricerca in corso

    # impostazione date, pre e post classifica
    if riga.year == 2015:
        # prima finestra
        # BUONO until1 = datetime(2015, 11, 16, 00, 00, 00)
        until1 = datetime(2015, 11, 16, 00, 00, 00)

        until1 = until1 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        # BUONO since1 = datetime(2015, 9, 1, 00, 00, 00)
        since1 = datetime(2015, 11, 15, 00, 00, 00)

        changing1 = until1 - timedelta(days=1)
        remaining_days1 = int(str(changing1 - since1).split()[0])

        # seconda finestra
        # BUONO until2 = datetime(2016, 2, 1, 00, 00, 00)
        until2 = datetime(2015, 11, 18, 00, 00, 00)

        until2 = until2 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        # BUONO since2 = datetime(2015, 11, 17, 00, 00, 00)
        since2 = datetime(2015, 11, 17, 00, 00, 00)

        changing2 = until2 - timedelta(days=1)
        remaining_days2 = int(str(changing2 - since2).split()[0])

    else:
        # prima finestra
        until1 = datetime(2019, 10, 15, 00, 00, 00)
        until1 = until1 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        since1 = datetime(2019, 8, 1, 00, 00, 00)
        changing1 = until1 - timedelta(days=1)
        remaining_days1 = int(str(changing1 - since1).split()[0])

        # seconda finestra
        until2 = datetime(2020, 1, 1, 00, 00, 00)
        until2 = until2 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        since2 = datetime(2019, 10, 16, 00, 00, 00)
        changing2 = until2 - timedelta(days=1)
        remaining_days2 = int(str(changing2 - since2).split()[0])

    nome_donna = riga.name
    username_donna = riga.username_twitter
    id_donna = riga.id

    # considero per ogni donna gli hashtag di bbc100women
    hashtags_considerati = ''
    user_mention_bbc = "@BBC100Women"
    hashtags_bbc = "#BBC100Women OR #BBC100women OR #bbc100women OR #Bbc100Women OR #bbc100WOMEN OR #bBc100women OR #BBC100WOMEN OR #100women"
    query_bbc = "{} OR {}".format(user_mention_bbc, hashtags_bbc)

    if pd.isna(riga.hashtag) is False:  # se la donna ha degli hashtag propri
        lista_hashtag = riga.hashtag.split()
        for element in lista_hashtag:
            hashtags_considerati = hashtags_considerati + element + ' OR '  # aggiungo agli hashtag della donna quelli della bbc
        hashtags_considerati = hashtags_considerati + query_bbc
    else:
        hashtags_considerati = query_bbc  # la donna non ha hashtag personali, utilizzo solo quelli della bcc

    if pd.isna(username_donna) is False:  # se la donna ha lo username
        query = "({} OR ({} AND ({})))".format(username_donna, nome_donna, hashtags_considerati)
    else:
        query = "({} AND ({}))".format(nome_donna, hashtags_considerati) # se la donna non ha lo username, cerco nome+hashtag

    print("\n\t\t\tINIZIO SCARICAMENTO PRIMA FINESTRA")
    df1 = scaricamento_tweets(until1, since1, changing1, remaining_days1, complete_tweets_db, query)  # in df1 salvo i tweet che sono stati trovati pre classifica
    print("\n\t\t\tFINE SCARICAMENTO PRIMA FINESTRA")
    if not df1.empty:
        print("\n--------------------> Ho trovato {} tweets pre classifica per {} <--------------------".format(df1.shape[0], nome_donna))
        df1.set_index('id', inplace=True)
        df1= df1[['date', 'tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']]  # i campi dei tweet che intendo memorizzare

        for tweet in df1.itertuples():
            if tweet not in donne_dictionary[id_donna]["tweets"]["pre-classifica"]:
                donne_dictionary[id_donna]["tweets"]["pre-classifica"].append(tweet)
    else:
        print("\n" "--------------------> Non ho trovato tweets pre classifica per {} <--------------------".format(nome_donna))


    print("\n\n\t\t\tINIZIO SCARICAMENTO SECONDA FINESTRA")
    df2 = scaricamento_tweets(until2, since2, changing2, remaining_days2, complete_tweets_db, query)  # in df2 salvo i tweet che sono stati trovati post classifica
    print("\n\t\t\tFINE SCARICAMENTO SECONDA FINESTRA")
    if not df2.empty:
        print("\n" "--------------------> Ho trovato {} tweets post classifica per {} <--------------------".format(df2.shape[0], nome_donna))
        df2.set_index('id', inplace=True)
        df2 = df2[['date', 'tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']]

        for tweet in df2.itertuples():
            if tweet not in donne_dictionary[id_donna]["tweets"]["post-classifica"]:
                donne_dictionary[id_donna]["tweets"]["post-classifica"].append(tweet)
    else:
        print("\n" "--------------------> Non ho trovato tweets post classifica per {} <--------------------".format(nome_donna))


print(donne_dictionary)

# salvataggio risultati
with open('results.json', 'w', encoding="UTF-8") as f:
    simplejson.dump(donne_dictionary, f, ignore_nan=True)

# # per fare merge di più parti
# with open('parte1.json') as f:
#     data1 = json.load(f)
#
# with open('parte2.json') as f:
#     data2 = json.load(f)
#
# output_final_merging = merge(data1, data2)