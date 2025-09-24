import argparse
import sys

program_name = sys.argv[0]

parser = argparse.ArgumentParser(
    prog=program_name,
    description="Dashboard para consultas sql de produtos da Amazon.",
    epilog="Use este parser apenas para fins de debug. O programa principal será iniciado pelo container.",
    usage='%(prog)s [options]'
)

parser.add_argument('--db-host',
                    type=str,
                    help='Host do banco de dados (localhost)',
                    default='localhost',
                    nargs='?'
                    )

parser.add_argument('--db-port',
                    type=int,
                    help='Porta do banco de dados (3306)',
                    default='3306',
                    nargs='?'
                    )

parser.add_argument('--db-name',
                    type=str,
                    help='Nome do banco de dados (ecommerce)',
                    default='ecommerce',
                    nargs='?'
                    )

parser.add_argument('--db-user',
                    type=str,
                    help='Usuário do banco de dados (postgres)',
                    default='postgres',
                    nargs='?'
                    )

parser.add_argument('--db-pass',
                    type=str,
                    help='Senha do banco de dados (postgres)',
                    default='postgres',
                    nargs='?'
                    )

parser.add_argument('--input',
                    type=str,
                    help='Arquivo de entrada',
                    nargs='?'
                    )

parser.add_argument('--product-asin',
                    type=str,
                    nargs='*',
                    help='ASIN do produto quando necessário'
                    )

parser.add_argument('--output',
                    type=str,
                    help='Arquivo de saída',
                    nargs='?'
                    )

results = parser.parse_args()

DB_HOST = results.db_host
DB_PORT = results.db_port
DB_NAME = results.db_name
DB_USER = results.db_user
DB_PASS = results.db_pass
INPUT = results.input
PRODUCT_ASIN = results.product_asin
OUTPUT = results.output