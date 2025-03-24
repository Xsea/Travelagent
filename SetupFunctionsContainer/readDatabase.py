import psycopg2

db_params = {
    'dbname': 'vectorDB',
    'user': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': 5432
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

select_query = 'SELECT * FROM space_travel_vectors WHERE chunk_id = 0;'
cursor.execute(select_query)
rows = cursor.fetchall()
for row in rows:
    print(row)