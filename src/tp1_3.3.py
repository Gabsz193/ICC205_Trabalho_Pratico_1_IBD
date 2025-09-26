import os

import pandas as pd
from pandas import DataFrame
import warnings

from args import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, PRODUCT_ASIN, OUTPUT
from db.connection import DatabaseConnection

databaseConnection = DatabaseConnection(
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASS
)

warnings.filterwarnings('ignore')

def get_df_from_query(query_file: str) -> DataFrame:
    try:
        with open(query_file, 'r') as f:
            query = f.read()
    except FileNotFoundError:
        print(f"Arquivo de query não encontrado: {query_file}")
        return pd.DataFrame()

    with databaseConnection as conn:
        query = query.replace(':asin_product', f'\'{PRODUCT_ASIN}\'')
        df = pd.read_sql_query(query, conn)
        return df

def list_consultas():
    return os.listdir('sql/consultas')

def main():
    consultas = list_consultas()

    for c in consultas:
        df = get_df_from_query(os.path.join('sql/consultas', c))
        print(f'Consulta do arquivo {c}')
        print(df)
        print('-'*30)
        csv_filename = c.replace('.sql', '.csv')
        df.to_csv(f'{OUTPUT}/{csv_filename}')


    exit(0)

if __name__ == '__main__':
    main()