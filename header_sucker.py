import sqlite3
from datetime import datetime
from random import randint
from time import sleep
import requests
from requests import adapters
import ssl
from urllib3 import poolmanager

class TLSAdapter(adapters.HTTPAdapter):
    """
    A TransportAdapter that turns security level down to avoid DH_KEY_TOO_SMALL errors .
    """
    def init_poolmanager(self, connections, maxsize, block=False):
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=context)

def save_headers(url, hdrs):
    scan_date = datetime.today().strftime('%m/%d/%Y')
    
    conn = sqlite3.connect("header.db")
    c = conn.cursor()
    for h in hdrs.keys():
        header_name = h
        header_value = hdrs[h]
        sql = "INSERT INTO headerz VALUES (null, :scan_date, :url, :header_name, :header_value)"
        c.execute(sql, {'url':url, 'scan_date':scan_date, 'header_name':header_name, 'header_value':header_value})
    conn.commit()

def get_headers(req_headers, url):
    try:    
        s = requests.Session()
        s.mount('https://', TLSAdapter())
        x = s.head(url, headers=req_headers, allow_redirects=True, verify=False)        
        #x = requests.head(url, headers=req_headers, allow_redirects=True, verify=False)
        save_headers(url,x.headers)
        print("saved headers of " + url)
    except Exception as e:
        print("error in " + url)
        print(e)
f = open("target_urls.txt")
temp = f.read().splitlines()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
req_headers = {
    'User-Agent': user_agent
}
for url in temp:
    hdrs = get_headers(req_headers, url)
    sleep(randint(1,2))

