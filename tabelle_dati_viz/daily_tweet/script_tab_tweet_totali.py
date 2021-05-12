"""
script R

library(forecast)
library(ggfortify)
library(zoo)
library(tseries)
library(astsa)
library(forecast)
library(ggplot2)
library(dplyr)
library(tidyr)

# genero le date per tutto l'anno (seq_full)
days <- seq(from = as.Date("2015-01-01"), 
                 to = as.Date("2015-12-31"), 
                 by = "days")
date_anno_intero <- data.frame(days)
write.csv(date_anno_intero,"seq_full.csv", row.names = FALSE)

# memorizzo tutte le date di pubblicazione dei tweet (seq_miss)
data2015 <- read.csv(file = 'tweets_2015.csv')
data2015 <- data2015[,c("date", "tweet")]
data2015[['date']] <- strptime(data2015[['date']], format='%Y-%m-%d  %H:%M:%S')
write.csv(data2015[,"date"],"seq_miss.csv", row.names = FALSE)

# conto per ogni giorno quanti tweet sono stati pubblicati (df)
data2015$day <- format(data2015$date, '%Y-%m-%d') # potrei ragionare a livello di giorno
data_day2015 <- count(data2015, day)
write.csv(data_day2015,"day2015_missing.csv", row.names = FALSE)

"""
import pandas as pd

seq_full = pd.read_csv("tabelle_dati_viz/seq_full.csv") # date di tutto l'anno
seq_full['days']= pd.to_datetime(seq_full['days'])

seq_miss = pd.read_csv("tabelle_dati_viz/seq_miss.csv") # date dei tweet
seq_miss.rename(columns = {'x' : 'day'}, inplace = True)
seq_miss['day']= pd.to_datetime(seq_miss['day'])

date_mancanti = pd.concat([seq_full, seq_miss]).drop_duplicates(keep=False) # date in cui ci sono 0 tweet
date_mancanti['n'] = 0

df = pd.read_csv("tabelle_dati_viz/day2015_missing.csv")  # date in cui ci sono n tweet, senza date con 0 tweet
merge = pd.concat([date_mancanti, df]) # merge date in cui ci sono 0 tweet e date in cui ci sono n tweet
merge['day'] =  pd.to_datetime(merge['day'], format='%Y-%m-%d')

merge = merge.sort_values(by = 'day')
merge.reset_index(inplace=True)
del merge['index']

merge.to_csv('2015.csv', index = False)


# eseguo tutto ciò per ogni anno

