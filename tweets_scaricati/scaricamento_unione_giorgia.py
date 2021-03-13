
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


def scaricamento_tweets(until, since, changing, remaining_days, complete_tweets_db):
    ##------------- ORA: Download dei tweets -------------##
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
        c.Pandas= True
        c.Count= True
        c.Hide_output= True
        # c.Store_json = True

        twint.run.Search(c)

        #complete_tweets_db=pd.DataFrame()
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


        # eliminazione dei duplicati
        complete_tweets_db_new_no_duplicates = complete_tweets_db[~complete_tweets_db.index.duplicated()]

    return complete_tweets_db_new_no_duplicates



# lista donne
df_lista_donne = pd.read_csv("tabella_finale_finale_RIDOTTA.csv", sep=';')
df_lista_donne.columns

df_lista_donne['hashtag_list'] = df_lista_donne.hashtag.str.split()

df_lista_ridotta = df_lista_donne[["id", "name", "username_twitter", "hashtag_list", "year"]]

# creazione struttura json da riempire con i tweets pre e post classifica
donne_dictionary = {}

for donna in df_lista_ridotta.itertuples():
  if donna[1] not in donne_dictionary:

    donne_dictionary[donna[1]] = {
        "tweets": {
            "pre-classifica": [],
            "post-classifica": []
        }
    }






###############################################################

##------------- ORA: Download dei tweets a partire dalla donna -------------##
for riga in df_lista_ridotta.itertuples():
    time.sleep(3)

    ### TEMPO ###

    # creo un nuovo dataset completo
    complete_tweets_db = pd.DataFrame()

    # impostazione date
    nest_asyncio.apply()  # Blocco eventuali loop di ricerca in corso

    if riga.year == 2015:
        # prima finestra
        until1 = datetime(2015, 11, 16, 00, 00, 00)
        until1 = until1 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
        since1 = datetime(2015, 9, 1, 00, 00, 00)
        changing1 = until1 - timedelta(days=1)
        remaining_days1 = int(str(changing1 - since1).split()[0])

        # seconda finestra
        until2 = datetime(2016, 2, 1, 00, 00, 00)
        until2 = until2 + timedelta(days=1)  # per considerare tutte le 24 ore del primo giorno
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

    #
    #
    # # per il 2015: https://www.bbc.com/news/world-34801473
    # # dal 18 novembre (data di pubblicazione) al 2 dicembre (data fine eventi legati a BBC100 Women)
    #
    # # Data inizio ricerca: la ricerca inizia dal giorno più recente
    # until = datetime(2015,11,17,0,0,0)
    # until = until + timedelta(days=1) # per considerare tutte le 24 ore del primo giorno
    # print("Until:    ", until)
    #
    # # Data fine ricerca: scaricamento tweets fino a questo data (più vecchia) rimane fissa
    # since = datetime(2015,11,10,00,00,00)
    #
    # # since = datetime(2015,1,1,00,00,00)
    # print("Since:    ", since)
    #
    # # Questo since è il giorno che continua a cambiare
    # changing = until - timedelta(days=1)
    # print("Changing: ", changing)
    #
    # # conteggio giorni rimanenti
    # remaining_days = int(str(changing-since).split()[0])
    #
    # ############################################################################
    # ############################################################################
    # ############################################################################

    ### RICERCA ###
    # hashtags = hash1 OR hash2
    #
    # username OR(name AND hashtags)
    #
    # (name AND hashtags)ORusername


    print("NOME DONNA: ", riga.name)
    print("NUOVA RICERCA")

    # ricerca tweet donna
    chiave = riga.name
    print(chiave)
    # user_mention = "@_antoniaalbert"
    # user_mention = username_twitter_uso
    user_mention = riga.username_twitter
    # hashtags_considerati = "Antonia Albert"
    # hashtags_considerati = lista_hashtag
    hashtags_considerati = riga.hashtag_list


    # query = "({} OR {})".format(user_mention, hashtags_considerati)
    query = "{}".format(user_mention)
    print(query)
    #
    # df1 = scaricamento_tweets(until1, since1, changing1, remaining_days1, 'pre', complete_tweets_db)
    # for tweet in df1.itertuples():
    #     # print(tweet)
    #     if tweet not in donne_dictionary[chiave]["tweets"]["pre-classifica"]:
    #         donne_dictionary[chiave]["tweets"]["pre-classifica"].append(tweet)
    #
    # df2 = scaricamento_tweets(until2, since2, changing2, remaining_days2, 'post', complete_tweets_db)
    # for tweet in df2.itertuples():
    #     # print(tweet)
    #     if tweet not in donne_dictionary[chiave]["tweets"]["post-classifica"]:
    #         donne_dictionary[chiave]["tweets"]["post-classifica"].append(tweet)
    #
    df1 = scaricamento_tweets(until1, since1, changing1, remaining_days1, complete_tweets_db)
    df1.set_index('id', inplace=True)
    df1= df1[['tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']]
    #try:
    for tweet in df1.itertuples():
            # print(tweet)
        print("3) ------------------ SONO QUI! ------------------")
        if tweet not in donne_dictionary[chiave]["tweets"]["pre-classifica"]:
            donne_dictionary[chiave]["tweets"]["pre-classifica"].append(tweet)
            print("Aggiunta in corso...")
    # except:
    #     continue

    df2 = scaricamento_tweets(until2, since2, changing2, remaining_days2, complete_tweets_db)
    df2.set_index('id', inplace=True)
    df2 = df2[['tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']]
    # try:
    for tweet in df2.itertuples():
        # print(tweet)
        print("4) ------------------ SONO QUI! ------------------")
        if tweet not in donne_dictionary[chiave]["tweets"]["post-classifica"]:
            donne_dictionary[chiave]["tweets"]["post-classifica"].append(tweet)
    #             print("Aggiunta in corso...")
    # except:
    #     continue

        #
        # # INSERIMENTO TWEETS IN DONNE-DICTIONARY
        # if complete_tweets_db_new_no_duplicates['tweet'].empty == False:
        #     for tweet in complete_tweets_db_new_no_duplicates['tweet']:
        #         # print(tweet)
        #         if tweet not in donne_dictionary[chiave]["tweets"]["pre-classifica"]:
        #             donne_dictionary[chiave]["tweets"]["pre-classifica"].append(tweet)
        # else:
        #     print("KEY NOT AVAILABLE!")
        #     continue
        # else:
        #   donne_dictionary[chiave]["tweets"]["pre-classifica"].append(tweet)
        # break
        # print("HO FINITO, RICERCO DONNA SUCCESSIVA!!!")
        #####################################################
        #####################################################
        #####################################################

with open('myfile_prova_dopo_ciclato_tabella.json', 'w', encoding="UTF-8") as f:
    simplejson.dump(donne_dictionary, f, ignore_nan=True)

print(donne_dictionary)