import json
import os

k = os.listdir('../downloader/jsons')
k = [i for i in k if i.endswith('.json')]

d = {}

for i in k:
    with open(f"../downloader/jsons/{i}", 'r') as json_file:
        metadata = json.load(json_file)
        for i in metadata:
            d[i] = metadata[i]

with open("output.json", "w") as json_file:
    json.dump(d, json_file, indent=4)