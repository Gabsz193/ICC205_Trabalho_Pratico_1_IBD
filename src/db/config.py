import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST : str = os.getenv("DB_HOST")
    DB_PORT : str = os.getenv("DB_PORT")
    DB_NAME : str = os.getenv("DB_NAME")
    DB_USER : str = os.getenv("DB_USER")
    DB_PASSWORD : str = os.getenv("DB_PASSWORD")
    if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]): 
        raise EnvironmentError("Erro ao setar variáveis de ambiente.\n"
                               "Verifique se em .env há os campos: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")