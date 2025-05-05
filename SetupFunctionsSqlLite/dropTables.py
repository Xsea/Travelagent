import sqlite3
con = sqlite3.connect("../travel.db")
cur = con.cursor()
cur.execute("DROP TABLE availabilities")