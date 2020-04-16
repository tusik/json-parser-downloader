# -*- coding: UTF-8 -*-
import psycopg2
import requests
import sys,json,os,re
from threading import Thread

def download_img(path,url):
    r = requests.get(url, headers=headers)
    filename_t = str(url).split('/')
    filename = filename_t[len(filename_t)-1]
    filename = re.sub('[\/:*?"<>|]','_',filename)
    with open(path+'/'+filename, 'wb') as f:
        f.write(r.content)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.149 Safari/537.36 '
}
title = ''
json_url = ''
if not os.path.exists("export.json"):
    r = requests.get(json_url, stream=True)
    f = open("export.json", "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
with open("export.json","r",encoding='utf-8') as data:
    json_obj = json.load(data)


for i in json_obj:
    title = i['title']
    title = re.sub('[\/:*?"<>|]','_',title)
    if not os.path.exists(title):
        os.mkdir(title)

    r = requests.get(i['cover'], headers=headers)
    with open(i['title']+"/cover.jpg", 'wb') as f:
        f.write(r.content)

    chaper = ''
    for k in i['chapters']:
        threads = []
        cp_title = k['title']
        cp_title = re.sub('[\/:*?"<>|]','_',cp_title)
        if os.path.exists(title+'/'+k['title']):
            cp_title = k['title']
        if not os.path.exists(title+'/'+cp_title):
            os.mkdir(title+'/'+cp_title)

        print('Downloading ' + cp_title)
        for j in k['images']:
            filename_t = str(j).split('/')
            filename = filename_t[len(filename_t)-1]
            if os.path.exists(title+'/'+cp_title+'/'+filename):
                continue

            t = Thread(target=download_img,args=[title+'/'+cp_title,j])
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

