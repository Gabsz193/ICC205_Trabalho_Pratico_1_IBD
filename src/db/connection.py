import psycopg2 as pg
from psycopg2.pool import SimpleConnectionPool
from db.config import Config

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
    def __init__(self):
        self._conn_stack: list[pg.extensions.connection] = []

    def __enter__(self) -> pg.extensions.connection:
        conn = _pool.getconn()
        self._conn_stack.append(conn)
        return conn

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._conn_stack:
            return
        conn = self._conn_stack.pop()
        if conn:
            try:
                if exc_type is None:
                    conn.commit()
                else:
                    conn.rollback()
            finally:
                _pool.putconn(conn)