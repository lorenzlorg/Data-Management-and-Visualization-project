In sintesi:
- partendo dai dati _dati_donne_indicatori_stati_ sono state create le _tabelle_finali_donne_indicatori_stati_ (contenenti i dati complessivi di donne, stati, indicatori stati)
- sono stati scaricati i tweets (_tweets_scaricati_) relativi all'evento BBC 100 Women per ogni anno (_tweets 2015-2020_) e i tweets associati alle singole donne (_tweets_donne_scaricati_)
- sono state apportate delle modifiche sui dati in modo tale che potessero essere usati per le visualizzazioni (_tabelle_dati_viz_)
- i dati sono stati raccolti in un'unica collezione in formato json, sottoforma di documenti annindati (_dati_formato_json_)

Le librerie utilizzate sono indicate in: _requirements_.
La versione di Python utilizzata è: 3.9

**cartella dati_donne_indicatori_stati**: sono contentute le liste BBC 100 Women per gli anni 2015 e 2019. La 
lista BBC 100 Women 2020 non è stata utilizzata per via del fatto che la scelta delle donne è stata fortemenete influenzata dalla situazione pandemica. 
Inoltre sono presenti le tabelle (e relativi script) con i dati relativi ai singoli indicatori degli Stati (hdi, gdp, gender gap ...). 

Il file _fonti_dati_integrazione_ contiene le fonti da cui sono stati scaricati i  vari indicatori e le liste BBC.


**cartella tabelle_finali_donne_indicatori_stati**: tramite lo script _integrazione_donne_indicatori_ vengono unite 
informazioni relative alle donne e informazioni relative agli Stati di appartenenza (gdp,gdp_pro_capita,labour_percentage,gender_gap,percentuale_ministre,
percentuale_parlamentari,hdi), il tutto presente nella cartella _dati_donne_indicatori_stati_. Questi dati sono relativi
agli anni 2015 e 2019. Si ottiene la tabella _indicatori_stati_nomidonne_v1_.
Da quest'ultima, apportando leggere modifiche , viene ricavata la tabella _indicatori_stati_nomidonne_v2_ ed essa viene utilizzata per viz relative agli indicatori.   
Inoltre viene creata a partire dalla tabella _info_identikit_donne_raw_v1_ (tramite lo script _integrazione_donne_indicatori_)
una nuova tabella _info_identikit_donne_raw_v2_, che contiene informazioni inserite manualmente (username Twitter, hashtags, account verificato, regione, categoria).
Una volta scaricati i tweets per ogni donna è stata creata la nuova tabella _info_identikit_donne_ utilizzata per le viz, inserendo
a partire da _info_identikit_donne_raw_v2_ e _tweets_scaricati/tweets_donne_pre_post.csv_ il numero di tweets pre e post pubblicazione della lista.


**cartella tabelle_dati_viz**: contiene le tabelle dati riadattate per consentire di effettuare le visualizzazioni in 
maniera più efficiente.  
- _daily_tweet_: per ogni anno (2015-2016-2017-2018-2019-2020), viene conteggiato il numero di tweets a livello giornaliero.
Vengono considerati anche i giorni in cui non sono presenti tweets. Questi dati servono per mostrare l'andamento
dei tweets durante l'anno. Le seguenti tabelle sono state ottenute  tramite manipolazione in R/Python dei file contenuti
in _tweets_scaricati/tweets 2015-2020_.

- _indicatori_stati_nomidonne_v2_: vengono utilizzati questi dati per viz indicatori e sono ricavati da _tabelle_finali_donne_indicatori_stati_

- _info_identikit_donne_: vengono utilizzati questi dati per identikit donne e sono ricavati da tabelle_finali_donne_indicatori_stati.
Viene inoltre utilizzata per valutare la differenza del numero di tweets pre e post pubblicazione della lista per ciascuna donna
(2015 e 2019). I campi presi in considerazione sono donna, numero tweet pre e post classifica.


**cartella tweets_scaricati**: vi sono tutti i tweets scaricati dal 2015 al 2020, utilizzando particolari hashtag relativi 
all'evento della bbc (il relativo script è _scaricamento_tweets_bbc100women_). Questi dati sono stati scaricati per capire 
l'andamento del numero di tweets pre e post pubblicazione della lista.   

Il file _scaricamento_tweets_donne_ è invece relativo allo scaricamento dei tweets per ogni donna (usando gli hashtags
della donna in questione oltre a quelli della BBC). Questi dati servono per capire come la popolarità delle donne è 
cambiata con la pubblicazione della lista.

Il file _tweets_donne_scaricati_ (vedi link) contiene dunque per ogni donna il conteggio dei tweets pre e post
uscita della lista, compresi tutti i tweets.

Il file _producer_tweets_kafka_ invece è lo script che permette di simulare la velocità interfacciandosi con Kafka.

Il file _Nifi_consumer_ è il workflow implementato in NiFi per la realizzazione del consumer. A sua volta quest'ultimo invierà i dati ad un database Mongo DB.

**cartella dati_formato_json**: a partire dai dati in _tabelle_finali_donne_indicatori_stati_ è stato creata la tabella
_dati_formato_json/indicatori_stati_nomidonne_v3.csv_. A seguire, utilizzando lo script _dati_formato_json/creazione_struttura_documento.py_,
è stato generato un file json comprensivo di tutti i dati relativi a donne e Stati, _countries_women.json_.
L'obiettivo era quello di utlizzare tale file per le viz ma come si è specificato nel report non è stato possibile processarlo tramite Tableau,
visti i suoi diversi livelli di annidamento e la sua dimensione non banale.


Per quanto riguarda le **visualizzazioni**:  

- per mostrare andamento tweets (heatmap): _tabelle_dati_viz/daily_tweet/num_tweet_daily_2015_2020.csv_,
  (dal 2015 al 2020)

- per mostrare variazione popolarità donne (bar chart e donut chart): _tabelle_finali_donne_indicatori_stati/info_identikit_donne.xlsx_, (2015 e 2019)

- per mostrare identikit donna (lollipop e alluvional): _tabelle_finali_donne_indicatori_stati/info_identikit_donne.xlsx_,
(2015 e 2019)

- per mostrare analisi indicatori (scatterplot): _tabelle_dati_viz/indicatori_stati_nomidonne_v2.csv_, (2015 e 2019)
