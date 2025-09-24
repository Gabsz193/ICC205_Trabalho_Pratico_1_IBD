from db.connection import DatabaseConnection
from args import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, INPUT
from parser.amazon_parser import AmazonParser


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

def parse_and_save(filename: str):
    amazon_parser = AmazonParser(filename)

    print(amazon_parser.get_count())



def main():
    try:
        with open('sql/schema.sql', 'r') as f:
            script = f.read()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return -1

    if create_tables(script) == -1:
       return -1

    parse_and_save(INPUT)

    return 0


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
