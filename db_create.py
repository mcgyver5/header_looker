import sqlite3

conn = sqlite3.connect("header.db")
c = conn.cursor()

sql = "CREATE TABLE headerz (header_id INTEGER PRIMARY KEY, date_seen text, url text, header_name text, value text)"

c.execute(sql)

conn.commit()


conn.close()



