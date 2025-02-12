import json
from operator import invert
import os
import re
from bs4 import BeautifulSoup
from math import log10, sqrt

directory = '../downloader/files'

k = os.listdir(directory)

NumDocs = len(k)

inverted_index = {}

c = 1
# calculating term counts
for i in k:
    print(c)
    print(i)
    f = open(f"{directory}/{i}").read()

    text = BeautifulSoup(f, "html.parser").text

    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text).casefold()

    for j in text.split():
        if j not in inverted_index:
            inverted_index[j] = {}
        inverted_index[j][i] = {"tf" : text.count(j)}
    
    c += 1

# calculating idfk score 
for i in inverted_index:
    nk = len(inverted_index[i])
    idfk = log10(NumDocs/nk)
    for j in inverted_index[i]:
        inverted_index[i][j]["w"] = inverted_index[i][j]["tf"] * idfk
    inverted_index[i]["idfk"] = idfk

normalization = {}

for i in inverted_index:
    for j in inverted_index[i]:
        if j != "idfk":
            normalization_val = normalization.get(j, 0)
            normalization_val += (inverted_index[i][j]["w"] ** 2)
            normalization[j] = normalization_val

for i in inverted_index:
    for j in inverted_index[i]:
        if j != "idfk":
            inverted_index[i][j]["d"] = sqrt(normalization[j])


with open("inv_index.json", "w") as json_file:
    json.dump(inverted_index, json_file, indent=4)