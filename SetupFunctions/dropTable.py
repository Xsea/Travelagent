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

try:
    print("Before")
    sql = '''DROP TABLE example_table '''
    cursor.execute(sql)
    print("Table killed")
    connection.commit()

    # Closing the connection
    connection.close()

except Exception as error:
    print(f"Error connecting to the database: {error}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed")