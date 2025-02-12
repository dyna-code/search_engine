from doctest import master
import requests
from bs4 import BeautifulSoup
import re
import os

def is_valid_domain(link):
    valid_domains = [
        "www.forbes.com"
    ]

    is_in_valid_domain = False

    for i in valid_domains:
        if i in link and 'www.forbes.com/video' not in link:
            is_in_valid_domain = True
        
    return is_in_valid_domain

def clean_link(link, cur_page):
    if link.startswith("http://") or link.startswith("https://"):
        return link

    elif is_valid_domain(link):
        return "https:" + link
    
    return cur_page + link

def normalize_link(link):
    if link.endswith('/') or link.endswith('#'):
        link = link[:-1]
    
    if link.startswith('http://'):
        link = 'https://' + link[7:]

    return link

def get_hrefs(link):
    try:
        html = requests.get(link, headers = headers, timeout = 0.7).text
        soup = BeautifulSoup(html, 'html.parser')
        hrefs = [[a['href'], a.text.replace("\n", "")] for a in soup.find_all('a', href=True)]
        hrefs = [i for i in hrefs if len(i[1].split()) > 2 and i[1][0].isupper()]
        return hrefs
    except:
        return []

def is_html(link):
    try:
        response = requests.head(link,timeout=0.7)
        return response.headers.get('Content-Type', '').lower().startswith('text/html')
    except:
        return False



headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"}

f = []
if os.path.isfile('links_forbes.txt'):
        with open('links_forbes.txt', 'r') as file:
            f = file.readlines()
            
url_queue = [i.strip().split() for i in f]
master_list = [i.strip().split() for i in f]


while url_queue and len(master_list) < 500:
    link = url_queue[0][0]
    hrefs = get_hrefs(link)
    for i in hrefs:
        if is_valid_domain(i[0]):
            pattern = r'(https:\/\/www\.forbes\.com\/sites\/([a-zA-Z0-9-]+)\/(\d{4}\/\d{2}\/\d{2})\/([a-zA-Z0-9-]+)\/)'
            matches = re.findall(pattern, i[0])

            if matches:
                new_link = matches[0][0]
                i[1] = i[1].replace("MORE FROM FORBES", "")
                if [new_link, i[1]] not in master_list:
                    master_list.append([new_link, i[1]])
                    url_queue.append([new_link, i[1]])


    url_queue.pop(0)

print((master_list))

f = open("links_forbes.txt", "w")

for i in master_list:
    f.write(i[0] + " " + i[1] + "\n")
f.close()



                