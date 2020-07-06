import sqlite3

conn = sqlite3.connect("header.db")

c = conn.cursor()


sql = "SELECT url, header_name, value from headerz "

c.execute(sql)
rowz = c.fetchall()
for r in rowz:
    hname = r[1]
    hvalue = r[2]
    url = r[0]
    print("{} - {}:{}".format(url,hname,hvalue))
