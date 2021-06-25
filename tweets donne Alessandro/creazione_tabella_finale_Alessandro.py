import pandas as pd

# Apertura e lettura file "tabella_finale_finale_V3.csv e "tweets_donne_scaricati_viz.csv"
df_csv = pd.read_csv('tweets donne Alessandro/tabella_finale_finale_V3_MOD_Alessandro.csv')
df_csv_women = pd.read_csv('tweets donne Alessandro/tweets_donne_scaricati_viz.csv')

# Rinomina colonne per poter poi droppare i doppioni
df_csv_women.rename(columns={'name': 'name_clean', 'Unnamed: 0': 'Unnamed_clean', 'id': 'id_clean'}, inplace=True)

# Riodino i dataframe in base al nome delle donne in ordine ascendente
sorted_df_1 = df_csv.sort_values(by='name')
sorted_df_2 = df_csv_women.sort_values(by=['name_clean', 'number_tweets_pre_ranking', 'number_tweets_post_ranking'])

# Concatenazione
horizontal_concat = pd.concat([sorted_df_1, sorted_df_2], axis=1).reindex(sorted_df_1.index)

# droppare le colonne non necessarie
horizontal_concat.drop(['name', 'Unnamed: 0', 'id'], axis=1)

# Riordino le colonne
horizontal_concat = horizontal_concat[['Unnamed_clean',
                                       'id_clean',
                                       'name_clean',
                                       'number_tweets_pre_ranking',
                                       'number_tweets_post_ranking',
                                       'age',
                                       'username_twitter',
                                       'hashtag',
                                       'job',
                                       'description',
                                       'image',
                                       'category',
                                       'country',
                                       'year',
                                       'gdp',
                                       'gdp_pro_capita',
                                       'labour_percentage',
                                       'gender_gap',
                                       'percentuale_ministre',
                                       'percentuale_parlamentari',
                                       'hdi']]

# Rinomina colonne
horizontal_concat.rename(columns={'name_clean': 'name', 'Unnamed_clean': 'Unnamed: 0', 'id_clean': 'id'},
                         inplace=True)

# Ordina nuovamente
horizontal_concat = horizontal_concat.sort_values(by='Unnamed: 0')

# Esporto il file finale creto
horizontal_concat.to_csv('final_table_Alessandro_no_cambio_nome_colonne.csv',
                         index=False,
                         encoding='UTF-8')
