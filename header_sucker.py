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

def save_headers(url, status_code, hdrs, url_id):
    scan_date = datetime.today().strftime('%m/%d/%Y')
    
    conn = sqlite3.connect("header.db")
    c = conn.cursor()
    for h in hdrs.keys():
        header_name = h
        header_value = hdrs[h]
        sql = "INSERT INTO header_collection VALUES (null, :scan_date, :header_name, :header_value, :status_code, :url_id)"
        c.execute(sql, {'scan_date':scan_date, 'header_name':header_name, 'header_value':header_value, 'status_code':status_code, 'url_id':url_id})
        if header_name == 'Content-Security-Policy':
            h_id = c.lastrowid
            csp_parts = header_value.split(";")
            csp_sql = "INSERT INTO cspval VALUES (null, :csp_piece, :h_id)"
            for csp_piece in csp_parts:
                c.execute(csp_sql, {'csp_piece':csp_piece.strip(), 'h_id':h_id})
    conn.commit()

def get_headers(req_headers, url,url_id):
    try:    
        s = requests.Session()
        s.mount('https://', TLSAdapter())
        x = s.head(url, headers=req_headers, allow_redirects=True,timeout=1.96, verify=False)        
        rcode = x.status_code
        if rcode == 405:
            x = s.get(url, headers=req_headers, allow_redirects=True, timeout=1.15, verify=False)
        save_headers(url,rcode,x.headers,url_id)
        print("saved headers of {} - response code: {} ".format(url, rcode) )
    except Exception as e:
        print("error in " + url)
        print(e)

url_sql = "SELECT url_id,url_text FROM short_list"
conn2 = sqlite3.connect("header.db")
cursor2 = conn2.cursor()
cursor2.execute(url_sql)
rows = cursor2.fetchall()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
req_headers = {
    'User-Agent': user_agent
}
for row in rows:
    url = row[1]
    url_id = row[0]
    hdrs = get_headers(req_headers, url, url_id)
    sleep(randint(1,4))

