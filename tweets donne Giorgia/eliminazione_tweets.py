import json

with open('output_prova_2.json', 'w') as w:
    with open('results_prova_2.json', 'r') as r:
        for line in r:
            element = json.loads(line.strip())
            del element["tweets"]
            w.write(json.dumps(element))

with open('output_prova.json', 'w') as w:
    with open('results_prova_2.json') as json_data:
        data = json.load(json_data)
        for element in data:
            del element['tweets']
        w.write(json.dumps(element))


with open('results_prova.json') as data_file:
    data = json.load(data_file)

for element in data:
    if 'pre-classifica' in element:
        del element['pre-classifica']
    if 'post-classifica' in element:
        del element['post-classifica']

with open('data.json', 'w') as data_file:
    data = json.dump(data, data_file)