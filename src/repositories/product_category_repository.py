from typing import Optional, List, Union

from models.product_category import ProductCategory
from repositories.base import BaseRepository


class ProductCategoryRepository(BaseRepository[ProductCategory]):
    TABLE_NAME: str = "Product_Category"

    def save(self, entity: Union[ProductCategory, List[ProductCategory]]) -> Union[ProductCategory, List[ProductCategory]]:
        if isinstance(entity, list):
            with self.connection as conn:
                with conn.cursor() as cursor:
                    return self._insert_all(cursor, entity)
        else:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    if self._exists(entity.id_product_category):
                        return self._update(cursor, entity)
                    else:
                        return self._insert(cursor, entity)

    def _insert_all(self, cursor, categories: List[ProductCategory]) -> List[ProductCategory]:
        placeholders = ','.join(['(%s, %s, %s)' for _ in categories])

        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_PRODUCT_CATEGORY, ID_PRODUCT, ID_CATEGORY)
            VALUES {placeholders}
            ON CONFLICT (ID_PRODUCT_CATEGORY) DO NOTHING 
        """

        params = []
        for p in categories:
            params.extend([
                p.id_product_category,
                p.id_product,
                p.id_category,
            ])

        cursor.execute(query, tuple(params))

        return categories

    def _insert(self, cursor, category: ProductCategory) -> ProductCategory:
        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_PRODUCT_CATEGORY, ID_PRODUCT, ID_CATEGORY)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            category.id_product_category,
            category.id_product,
            category.id_category,
        ))
        return category

    def _update(self, cursor, category: ProductCategory) -> ProductCategory:
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET ID_PRODUCT = %s, ID_CATEGORY = %s
            WHERE ID_PRODUCT_CATEGORY = %s;
        """
        cursor.execute(query, (
            category.id_product,
            category.id_category,
            category.id_product_category,
        ))
        return category

    def _exists(self, id_product_category: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID_PRODUCT_CATEGORY FROM {self.TABLE_NAME} WHERE ID_PRODUCT_CATEGORY = %s",
                    (id_product_category,),
                )
                return cursor.fetchone() is not None

    def find_by_id(self, id_value: str) -> Optional[ProductCategory]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ID_PRODUCT_CATEGORY = %s",
                    (id_value,),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_all(self) -> List[ProductCategory]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                return [self._map_to_entity(row) for row in cursor.fetchall()]

    def delete(self, id_value: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE ID_PRODUCT_CATEGORY = %s",
                    (id_value,),
                )
                return cursor.rowcount > 0

    def _map_to_entity(self, row) -> ProductCategory:
        return ProductCategory(
            id_product_category=row[0],
            id_product=row[1],
            id_category=row[2],
        )