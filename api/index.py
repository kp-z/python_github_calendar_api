# -*- coding: UTF-8 -*-
pip install beautifulsoup4
import requests
from http.server import BaseHTTPRequestHandler
import json
from bs4 import BeautifulSoup

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]

def getdata(name):
    headers = {
        'Referer': 'https://github.com/'+ name,
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'X-Requested-With': 'XMLHttpRequest'
    }

    gitpage = requests.get("https://github.com/" + name  + "?action=show&controller=profiles&tab=contributions&user_id="+ name, headers=headers)
    data = gitpage.text

    soup = BeautifulSoup(data, 'html.parser')
    contributions = soup.find_all('rect')

    datadate = [contrib['data-date'] for contrib in contributions]
    datacount = [int(contrib['data-count']) for contrib in contributions]

    if not datadate or not datacount:
        return {"total": 0, "contributions": []}

    sorted_data = sorted(zip(datadate, datacount))
    datadate, datacount = zip(*sorted_data)

    contributions = sum(datacount)
    datalist = []
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    return returndata

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        spl=path.split('?')[1:]
        for kv in spl:
            key,user=kv.split("=")
            if key=="user": break
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
