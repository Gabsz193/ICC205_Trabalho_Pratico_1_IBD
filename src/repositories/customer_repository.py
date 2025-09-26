from typing import Optional, List, Union

from models.customer import Customer
from repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    TABLE_NAME: str = "Customer"

    def save(self, entitity: Union[Customer, List[Customer]]) -> Union[Customer, List[Customer]]:
        if isinstance(entitity, list):
            with self.connection as conn:
                with conn.cursor() as cursor:
                    return self._insert_all(cursor, entitity)
        else:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    if self._exists(entitity.id_customer):
                        return self._update(cursor, entitity)
                    else:
                        return self._insert(cursor, entitity)

    def _insert_all(self, cursor, customers: List[Customer]) -> List[Customer]:
        placeholders = ','.join(['(%s)' for _ in customers])

        query = f"""
                    INSERT INTO {self.TABLE_NAME} (ID_CUSTOMER)
                    VALUES {placeholders}
                    ON CONFLICT (ID_CUSTOMER) DO NOTHING 
                """

        params = []
        for p in customers:
            params.extend([
                p.id_customer,
            ])

        cursor.execute(query, tuple(params))

        return customers


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