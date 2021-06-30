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


def download_tweets(until, since, changing, remaining_days, complete_tweets_db, query):

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

        try:
            twint.run.Search(c)
        except:
            twint.run.Search(c)

        print(twint.storage.panda.Tweets_df.shape)

        # Importo i dati giornalieri nel dataframe completo
        complete_tweets_db = complete_tweets_db.append(twint.storage.panda.Tweets_df)
        print(complete_tweets_db.shape)
        #print(complete_tweets_db.columns)

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

    # complete_tweets_db_new_no_duplicates = complete_tweets_db[~complete_tweets_db.index.duplicated()]

    return complete_tweets_db

    #return complete_tweets_db_new_no_duplicates


# lista donne bbc
df_women = pd.read_excel("tabelle_finali_donne_indicatori_stati/info_identikit_donne_raw_v2.xlsx")
df_women_redux = df_women[["id", "name", "username_twitter", "hashtag", "year"]]

documents=[]
# Download dei tweets e creazione documento
for row in df_women_redux.itertuples():

    print("\n\n" + "*"*50 + row.name + "*"*50)

    complete_tweets_db = pd.DataFrame()  # creo un nuovo dataset completo
    nest_asyncio.apply()  # Blocco eventuali loop di ricerca in corso

    # impostazione date, pre e post classifica
    if row.year == 2015:
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

    name = row.name
    username = row.username_twitter
    id_woman = row.id

    # considero per ogni donna gli hashtag di bbc100women
    hashtags_considered = ''
    user_mention_bbc = "@BBC100Women"
    hashtags_bbc = "#BBC100Women OR #BBC100women OR #bbc100women OR #Bbc100Women OR #bbc100WOMEN OR #bBc100women OR #BBC100WOMEN OR #100women"
    query_bbc = "{} OR {}".format(user_mention_bbc, hashtags_bbc)

    if pd.isna(row.hashtag) is False:  # se la donna ha degli hashtag propri
        list_hashtag = row.hashtag.split()
        for element in list_hashtag:
            hashtags_considered = hashtags_considered + element + ' OR '  # aggiungo agli hashtag della donna quelli della bbc
        hashtags_considered = hashtags_considered + query_bbc
    else:
        hashtags_considered = query_bbc  # la donna non ha hashtag personali, utilizzo solo quelli della bcc

    if pd.isna(username) is False:  # se la donna ha lo username
        query = "({} OR ({} AND ({})))".format(username, name, hashtags_considered)
    else:
        query = "({} AND ({}))".format(name, hashtags_considered) # se la donna non ha lo username, cerco nome+hashtag

    document = {
        'id': id_woman,
        'name': name,
        "number_tweets_pre_ranking": 0,
        "number_tweets_post_ranking": 0,
        'tweets': {
            "pre_ranking": [],
            "post_ranking": []
        }
    }

    # adesso considero le finestre temporali separatamente
    print("\n\n\t\t\tINIZIO SCARICAMENTO PRIMA FINESTRA")
    df1 = download_tweets(until1, since1, changing1, remaining_days1, complete_tweets_db,
                              query)  # in df1 salvo i tweet che sono stati trovati pre classifica
    print("\n\t\t\tFINE SCARICAMENTO PRIMA FINESTRA")

    print("\n\n\t\t\tINIZIO SCARICAMENTO SECONDA FINESTRA")
    df2 = download_tweets(until2, since2, changing2, remaining_days2, complete_tweets_db,
                              query)  # in df2 salvo i tweet che sono stati trovati post classifica
    print("\n\t\t\tFINE SCARICAMENTO SECONDA FINESTRA")

    print("\n\t\t\tVERIFCO PRESENZA DUPLICATI")
    # se entrambi non sono vuoti dobbiamo verificare che non ci siano duplicati, se uno dei due è vuoto non mi pongo il problema e non eseguo questa parte di codice
    if not df1.empty and not df2.empty:
        df1['type'] = 'df1'
        df2['type'] = 'df2'
        concatenated = pd.concat([df1, df2])
        # concatenated.drop_duplicates(subset="id", keep="first", inplace=True)
        concatenated_clean = concatenated.drop_duplicates(subset="id", keep="first", inplace=False)
        if concatenated.shape != concatenated_clean.shape:
            print("ho trovato ed eliminato alcuni duplicati")
        else:
            print("non ho trovato duplicati")
        df1 = concatenated_clean.loc[concatenated['type'] == "df1"] # df1 pulito
        df2 = concatenated_clean.loc[concatenated['type'] == "df2"] # df2 pulito


    if not df1.empty:
        print("\n--------------------> Ho trovato {} tweets pre classifica per {} <--------------------".format(
            df1.shape[0], name))
        document["number_tweets_pre_ranking"] = df1.shape[0]
        df1.set_index('id', inplace=True)
        df1 = df1[['date', 'tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies',
                   'nretweets']]  # i campi dei tweet che intendo memorizzare - cosi elimino anche l'eventuale colonna "type"

        for tweet in df1.itertuples():
            if tweet not in document["tweets"]["pre_ranking"]:
                document["tweets"]["pre_ranking"].append(tweet)
    else:
        print("\n" "--------------------> Non ho trovato tweets pre classifica per {} <--------------------".format(name))


    if not df2.empty:
        print("\n" "--------------------> Ho trovato {} tweets post classifica per {} <--------------------".format(
            df2.shape[0], name))
        document["number_tweets_post_ranking"] = df2.shape[0]
        df2.set_index('id', inplace=True)
        df2 = df2[
            ['date', 'tweet', 'language', 'hashtags', 'user_id', 'username', 'name', 'nlikes', 'nreplies', 'nretweets']]

        for tweet in df2.itertuples():
            if tweet not in document["tweets"]["post_ranking"]:
                document["tweets"]["post_ranking"].append(tweet)
    else:
        print("\n" "--------------------> Non ho trovato tweets post classifica per {} <--------------------".format(name))

    documents.append(document)

# salvataggio risultati
with open('tweets_donne_scaricati.json', 'w', encoding="UTF-8") as f:
    simplejson.dump(documents, f, ignore_nan=True)


# per fare merge di più parti
# files=['parte_1.json','parte_2.json','parte_3.json']
# def merge_JsonFiles(filename):
#     result = list()
#     for f1 in filename:
#         with open(f1, 'r') as infile:
#             result.extend(json.load(infile))
#     with open('final_output', 'w') as output_file:
#         json.dump(result, output_file)
# merge_JsonFiles(files)


# per creare una versione dei dati adatta per le visualizzazioni

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
with open('tweets_donne_scaricati_viz.json', 'w', encoding="UTF-8") as f:
    simplejson.dump(copia_json, f, ignore_nan=True)

# Riapro il file salvato
with open('tweets_donne_scaricati_viz.json') as json_file:
    data_da_convertire = json.load(json_file)

# creo un oggetto e lo esporto in csv
pdObj = pd.read_json('tweets_donne_scaricati_viz.json')
export_csv = pdObj.to_csv ('tweets_donne_pre_post.csv', header=True)

pdObj.to_csv(index=False)