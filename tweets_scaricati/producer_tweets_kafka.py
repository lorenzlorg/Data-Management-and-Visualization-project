# il seguente script viene eseguito per ogni singolo anno considerato (di seguito viene riportato lo script per l'anno 2020)
# da utilizzare su jupyterlab tramite macchina virtuale Azure

# !pip3 install git+https://github.com/dpkp/kafka-python
from kafka import KafkaProducer
import json
import time

# producer creation
producer = KafkaProducer(
    bootstrap_servers = ["kafka:9092"],
    value_serializer = lambda v: json.dumps(v).encode("UTF-8"))

# lettura file json tweets scaricati
tweets_final = json.load(open("tweets_2020.json"))

# tweets -> topic -> mongodb
for tweet in tweets_final:
    # print(tweet)
    producer.send(topic='tweets', value=tweet)
    # print("tweet delivered")
    # time.sleep(0.15)