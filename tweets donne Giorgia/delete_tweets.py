import os
import json

tweets = "tweets"
with open('final_output.json', 'r') as dataFile:
    data = json.load(dataFile)

# print(data)
if tweets in data:
    del data[tweets]

# print(data)
with open('output_redux.json', 'w') as dataFile:
    data = json.dump(data, dataFile)



import json

with open('final_output.json') as data_file:
    data = json.load(data_file)

for element in data:
    del element['tweets']

with open('data_redux.json', 'w') as data_file:
    data = json.dump(data, data_file)