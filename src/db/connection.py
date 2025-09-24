import psycopg2 as pg
from psycopg2.pool import SimpleConnectionPool
from db.config import Config


class DatabaseConnection:
    _pool: SimpleConnectionPool = None

    def __init__(self, db_host=None, db_port=None, db_name=None, db_user=None, db_password=None):
        config = Config(db_host, db_port, db_name, db_user, db_password)

        self._pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_NAME
        )
        self._conn_stack: list[pg.extensions.connection] = []

    def __enter__(self) -> pg.extensions.connection:
        conn = self._pool.getconn()
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
                self._pool.putconn(conn)
