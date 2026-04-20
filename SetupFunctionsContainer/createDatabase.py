try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

import sqlite_vec

con = sqlite3.connect("../travel.db")
con.enable_load_extension(True)
sqlite_vec.load(con)
con.enable_load_extension(False)

print("Connected to travel.db")

con.execute("DROP TABLE IF EXISTS space_travel_vectors")
con.execute("""
    CREATE VIRTUAL TABLE space_travel_vectors USING vec0(
        id INTEGER PRIMARY KEY,
        name TEXT,
        chunk_id INTEGER,
        embedding float[3072]
    )
""")
con.commit()
print("Table space_travel_vectors created successfully")

con.close()
print("Database connection closed")
