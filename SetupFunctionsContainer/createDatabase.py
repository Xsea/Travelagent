import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'vectorDB',
    'user': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': 5432
}

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Connected to the database")

    # Example: Create a table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS space_travel_vectors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(256),
        chunk_id int,
        vector_column VECTOR(3072)
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully")

    # Example: Insert data into the table
    #insert_query = '''
    #INSERT INTO example_table (name, vector_column)
    #VALUES (%s, %s);
    #'''
    #cursor.execute(insert_query, ('example_name', '[1, 2, 3]'))
    #connection.commit()
    #print("Data inserted successfully")

    # Example: Query data from the table
    #select_query = 'SELECT * FROM example_table;'
    #cursor.execute(select_query)
    #rows = cursor.fetchall()
    #for row in rows:
    #    print(row)

except Exception as error:
    print(f"Error connecting to the database: {error}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Database connection closed")