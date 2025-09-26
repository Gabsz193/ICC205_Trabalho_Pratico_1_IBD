import argparse
import os
import sys

program_name = sys.argv[0]

parser = argparse.ArgumentParser(
    prog=program_name,
    description="Dashboard para consultas sql de produtos da Amazon.",
    epilog="Use este parser apenas para fins de debug. O programa principal será iniciado pelo container.",
    usage="\ndocker compose run --rm app python src/tp1_3.2.py --input <data_set_dir> [options]\n"
          "docker compose run --rm app python src/tp1_3.3.py --output <output_dir> [options]"
)

parser.add_argument('--db-host',
                    type=str,
                    help='Host do banco de dados (localhost)',
                    default=os.environ.get('DB_HOST', 'localhost'),
                    nargs='?'
                    )

parser.add_argument('--db-port',
                    type=int,
                    help='Porta do banco de dados (5432)',
                    default=os.environ.get('DB_PORT', 5432),
                    nargs='?'
                    )

parser.add_argument('--db-name',
                    type=str,
                    help='Nome do banco de dados (ecommerce)',
                    default=os.environ.get('DB_NAME', 'ecommerce'),
                    nargs='?'
                    )

parser.add_argument('--db-user',
                    type=str,
                    help='Usuário do banco de dados (postgres)',
                    default=os.environ.get('DB_USER', 'postgres'),
                    nargs='?'
                    )

parser.add_argument('--db-pass',
                    type=str,
                    help='Senha do banco de dados (postgres)',
                    default=os.environ.get('DB_PASS', 'postgres'),
                    nargs='?'
                    )

parser.add_argument('--input',
                    type=str,
                    help='Arquivo de entrada',
                    nargs='?',
                    default='data/amazon-meta.txt'
                    )

parser.add_argument('--product-asin',
                    type=str,
                    nargs='*',
                    help='ASIN do produto quando necessário',
                    default='0827229534'
                    )

parser.add_argument('--output',
                    type=str,
                    help='Arquivo de saída',
                    default='out',
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