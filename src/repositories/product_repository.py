from typing import Optional, List, overload, Union

from models.product import Product
from repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    TABLE_NAME: str = "Product"

    def save(self, entity: Union[Product, List[Product]]) -> Union[Product, List[Product]]:
        if isinstance(entity, list):
            with self.connection as conn:
                with conn.cursor() as cursor:
                    return self._insert_all(cursor, entity)
        else:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    if self._exists(entity.id_product):
                        return self._update(cursor, entity)
                    else:
                        return self._insert(cursor, entity)

    def _insert_all(self, cursor, products: List[Product]) -> List[Product]:
        placeholders = ','.join(['(%s, %s, %s, %s, %s, %s, %s)' for _ in products])

        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_PRODUCT, ASIN, TITLE, ID_GROUP, SALESRANK, TOTAL, AVG_RATING)
            VALUES {placeholders}
        """
        params = []

        for p in products:
            # garantir a ordem correta dos campos
            params.extend([
                p.id_product,
                p.asin,
                p.title,
                p.id_group,
                p.salesrank,
                p.total,
                p.avg_rating,
            ])
        cursor.execute(query, tuple(params))

        return products

    def _insert(self, cursor, product: Product) -> Product:
        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_PRODUCT, ASIN, TITLE, ID_GROUP, SALESRANK, TOTAL, AVG_RATING)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            product.id_product,
            product.asin,
            product.title,
            product.id_group,
            product.salesrank,
            product.total,
            product.avg_rating,
        ))

        return product

    def _update(self, cursor, product: Product) -> Product:
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET TITLE = %s, ID_GROUP = %s, SALESRANK = %s, TOTAL = %s, AVG_RATING = %s
            WHERE ID_PRODUCT = %s;
        """

        cursor.execute(query, (
            product.title,
            product.id_group,
            product.salesrank,
            product.total,
            product.avg_rating,
            product.id_product,
        ))

    def _exists(self, id_product: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID_PRODUCT FROM {self.TABLE_NAME} WHERE ID_PRODUCT = %s",
                    (id_product,),
                )
                return cursor.fetchone() is not None

    def find_by_id(self, id_value: str) -> Optional[Product]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ID_PRODUCT = %s",
                    (id_value,),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_by_asin(self, asin: str) -> Optional[Product]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ASIN = %s",
                    (asin,),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_all(self) -> List[Product]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                return [self._map_to_entity(row) for row in cursor.fetchall()]

    def delete(self, id_value: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE ID_PRODUCT = %s",
                    (id_value,),
                )
                return cursor.rowcount > 0

    def _map_to_entity(self, row) -> Product:
        return Product(
            id_product=row[0],
            asin=row[1],
            title=row[2],
            id_group=row[3],
            salesrank=row[4],
            total=row[5],
            avg_rating=row[6],
        )

