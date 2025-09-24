from db.connection import DatabaseConnection
from args import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS


def create_tables(script: str):
    try:
        with DatabaseConnection(
                DB_HOST,
                DB_PORT,
                DB_NAME,
                DB_USER,
                DB_PASS
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(script)
        return 0
    except Exception as e:
        print(e)
        return -1


def main():
    try:
        with open('sql/schema.sql', 'r') as f:
            script = f.read()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return -1

    return create_tables(script)


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
