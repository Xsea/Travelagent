import sqlite3
con = sqlite3.connect("../travel.db")
cur = con.cursor()

res = cur.execute("SELECT * FROM availabilities")
rows = res.fetchall()
for row in rows:
    print(row)