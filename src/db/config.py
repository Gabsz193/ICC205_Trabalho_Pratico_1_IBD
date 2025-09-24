import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    def __init__(self,
                 db_host=None,
                 db_port=None,
                 db_name=None,
                 db_user=None,
                 db_password=None):
        self.DB_HOST = db_host or self.DB_HOST
        self.DB_PORT = db_port or self.DB_PORT
        self.DB_NAME = db_name or self.DB_NAME
        self.DB_USER = db_user or self.DB_USER
        self.DB_PASSWORD = db_password or self.DB_PASSWORD

        if not all([self.DB_HOST, self.DB_PORT, self.DB_NAME, self.DB_USER, self.DB_PASSWORD]):
            raise EnvironmentError("Erro ao setar variáveis de ambiente.\n"
                                   "Verifique se em .env há os campos: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD")
