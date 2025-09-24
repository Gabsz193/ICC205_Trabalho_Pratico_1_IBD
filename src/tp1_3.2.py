from db.connection import DatabaseConnection
from args import *


def create_tables(script: str):
    with DatabaseConnection(
        DB_HOST,
        DB_PORT,
        DB_NAME,
        DB_USER,
        DB_PASS
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(script)



    pass

def main():
    try:
        with open('sql/schema.sql', 'r') as f:
            script = f.read()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return -1

    create_tables(script)

    return 0

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)