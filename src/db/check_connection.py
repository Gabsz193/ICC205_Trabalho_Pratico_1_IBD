from connection import DatabaseConnection

with DatabaseConnection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT version()")
        print(cursor.fetchone()[0])