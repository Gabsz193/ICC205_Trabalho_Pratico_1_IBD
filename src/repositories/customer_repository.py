from typing import Optional, List

from models.customer import Customer
from repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    TABLE_NAME: str = "Customer"

    def save(self, customer: Customer) -> Customer:
        with self.connection as conn:
            with conn.cursor() as cursor:
                if self._exists(customer.id_customer):
                    return self._update(cursor, customer)
                else:
                    return self._insert(cursor, customer)

    def _insert(self, cursor, customer: Customer) -> Customer:
        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_CUSTOMER)
            VALUES (%s)
        """
        cursor.execute(query, (customer.id_customer,))
        return customer

    def _update(self, cursor, customer: Customer) -> Customer:
        # Como só existe id_customer, não há nada para atualizar
        return customer

    def _exists(self, id_customer: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID_CUSTOMER FROM {self.TABLE_NAME} WHERE ID_CUSTOMER = %s",
                    (id_customer,),
                )
                return cursor.fetchone() is not None

    def find_by_id(self, id_value: str) -> Optional[Customer]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ID_CUSTOMER = %s",
                    (id_value,),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_all(self) -> List[Customer]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                return [self._map_to_entity(row) for row in cursor.fetchall()]

    def delete(self, id_value: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE ID_CUSTOMER = %s",
                    (id_value,),
                )
                return cursor.rowcount > 0

    def _map_to_entity(self, row) -> Customer:
        return Customer(
            id_customer=row[0],
        )