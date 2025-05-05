import sqlite3
con = sqlite3.connect("../travel.db")
cur = con.cursor()
#cur.execute("CREATE TABLE hotels(id INTEGER PRIMARY KEY, name VARCHAR(256), location VARCHAR(256), descriptionFile VARCHAR(256), price INT)")
cur.execute("CREATE TABLE availabilities(name VARCHAR(256), start DATE, end DATE)")

res = cur.execute("SELECT name FROM sqlite_master")
rows = res.fetchall()
for row in rows:
    print(row)