from math import sqrt
from flask import Flask, redirect, url_for, render_template, session, request
import json 
app = Flask(__name__)

def give_docs(query_vec, data):
    list_of_docs = []

    for i in query_vec:
        if i in data:
            list_of_docs.append(list(data[i].keys()))

    base = list_of_docs[0]
    final = []
    for i in base:
        is_in = True

        for j in list_of_docs[1:]:
            if i not in j:
                is_in = False
        
        if is_in:
            final.append(i)
    
    final = [i for i in final if i != 'idfk']

    return final

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        with open('../json_compiler/output.json', 'r') as json_file:
            metadata = json.load(json_file)
        with open('../inverted_index/inv_index.json', 'r') as json_file:
            data = json.load(json_file)

        query = request.form["search_query"]
        print(query)
        lean = request.form["search_type"]
        print(lean)

        rankings = [0.05, 0.125, 0.25, 0.375, 0.5, 0.375, 0.25, 0.125, 0.05]
        keys = ["Far Left", "Left", "Moderate", "Right", "Far Right"]
        values = rankings[int(lean) : int(lean) + 5]

        rankings_dict = dict(zip(keys, values))

        domain_split = {
            "vox": "Far Left",
            "newyorker": "Far Left",
            "cnn": "Left",
            "nbc": "Left",
            "forbes": "Moderate",
            "bbc": "Moderate",
            "foxbusiness": "Right",
            "oan": "Far Right",
            "nypost": "Right",
            "dailycaller": "Far Right"
        }
        
        fixname = {
            "vox": "Vox",
            "newyorker": "New Yorker",
            "cnn": "CNN",
            "nbc": "NBC",
            "forbes": "Forbes",
            "bbc": "BBC",
            "foxbusiness": "Fox Business",
            "oan": "OAN",
            "nypost": "NY Post",
            "dailycaller": "Daily Caller"
        }
        query_vec = list(set(query.split()))

        for i in query_vec:
            if i not in data:
                return "Sorry, these search term(s) are not available"

        list_of_docs = give_docs(query_vec, data)

        new_q_v = []

        for i in query_vec:
            new_q_v.append(data[i]["idfk"])
        
        norm_fac_q = 0
        for i in new_q_v:
            norm_fac_q += (i ** 2)
        
        norm_fac_q = sqrt(norm_fac_q)

        output = []

        for i in list_of_docs:
            temp_v_for_doc = []
            for j in query_vec:
                temp_v_for_doc.append(data[j][i]["tf"] * data[j]["idfk"])
                norm_fac_d = data[j][i]["d"]
            
            numerator = 0
            for j in range(len(new_q_v)):
                numerator += (new_q_v[j] * temp_v_for_doc[j])
            
            domain_rank = rankings_dict[domain_split[i.split("_")[0]]]
            output.append({"score" : 0.2*domain_rank + 0.8*(numerator/(norm_fac_q * norm_fac_d)), "title": metadata[f"files/{i}"]["title"], "file": url_for('static', filename = i), "domain": fixname[i.split("_")[0]], "lean": domain_split[i.split("_")[0]]})
        
        output.sort(key = lambda x : x["score"], reverse = True)
        
        print(output)
        stat = f'Searching for "{query}" with Political lean {keys[4 - int(lean)]}'
        return render_template("index.html", output = output, data = True, statement = stat)
    else:
        return render_template("index.html", data = False)

if __name__ == '__main__':
    app.run(debug=True)