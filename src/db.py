import psycopg2 as pg
from psycopg2.pool import SimpleConnectionPool
from config import Config

_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    database=Config.DB_NAME
)

class DatabaseConnection:
    def __enter__(self) -> pg.extensions.connection:
        self.conn = _pool.getconn()
        return self.conn
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
                
            _pool.putconn(self.conn)