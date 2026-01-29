import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="resultdb",
        user="leena",
        password="root",
        host="localhost",
        port="5432"
    )