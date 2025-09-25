from typing import Optional, List, Union

from models.similar_products import SimilarProducts
from repositories.base import BaseRepository


class SimilarProductsRepository(BaseRepository[SimilarProducts]):
    TABLE_NAME: str = "Similar_Products"

    def save(self, entitity: Union[SimilarProducts, List[SimilarProducts]]) -> Union[SimilarProducts, List[SimilarProducts]]:
        if isinstance(entitity, list):
            with self.connection as conn:
                with conn.cursor() as cursor:
                    return self._insert_all(cursor, entitity)
        else:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    if self._exists(entitity.id_product, entitity.id_similar_product):
                        return self._update(cursor, entitity)
                    else:
                        return self._insert(cursor, entitity)

    def _insert_all(self, cursor, similar: List[SimilarProducts]) -> List[SimilarProducts]:
        placeholders = ','.join(['(%s, %s, %s)' for _ in similar])

        query = f"""
                            INSERT INTO {self.TABLE_NAME} (ID_PRODUCT, ID_SIMILAR_PRODUCT, RANK)
                            VALUES {placeholders}
                        """
        params = []

        for p in similar:
            # garantir a ordem correta dos campos
            params.extend([
                p.id_product,
                p.id_similar_product,
                p.rank,
            ])
        cursor.execute(query, tuple(params))

        return similar

    def _insert(self, cursor, similar: SimilarProducts) -> SimilarProducts:
        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_PRODUCT, ID_SIMILAR_PRODUCT, RANK)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            similar.id_product,
            similar.id_similar_product,
            similar.rank,
        ))
        return similar

    def _update(self, cursor, similar: SimilarProducts) -> SimilarProducts:
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET RANK = %s
            WHERE ID_PRODUCT = %s AND ID_SIMILAR_PRODUCT = %s;
        """
        cursor.execute(query, (
            similar.rank,
            similar.id_product,
            similar.id_similar_product,
        ))
        return similar

    def _exists(self, id_product: str, id_similar_product: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID_PRODUCT FROM {self.TABLE_NAME} WHERE ID_PRODUCT = %s AND ID_SIMILAR_PRODUCT = %s",
                    (id_product, id_similar_product),
                )
                return cursor.fetchone() is not None

    def find_by_id(self, id_product: str, id_similar_product: str) -> Optional[SimilarProducts]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ID_PRODUCT = %s AND ID_SIMILAR_PRODUCT = %s",
                    (id_product, id_similar_product),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_all(self) -> List[SimilarProducts]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                return [self._map_to_entity(row) for row in cursor.fetchall()]

    def delete(self, id_product: str, id_similar_product: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE ID_PRODUCT = %s AND ID_SIMILAR_PRODUCT = %s",
                    (id_product, id_similar_product),
                )
                return cursor.rowcount > 0

    def _map_to_entity(self, row) -> SimilarProducts:
        return SimilarProducts(
            id_product=row[0],
            id_similar_product=row[1],
            rank=row[2],
        )