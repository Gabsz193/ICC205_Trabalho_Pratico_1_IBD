from typing import Optional, List

from models.category import Category
from repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    TABLE_NAME: str = "Category"

    def save(self, category: Category) -> Category:
        with self.connection as conn:
            with conn.cursor() as cursor:
                if self._exists(category.id_category):
                    return self._update(cursor, category)
                else:
                    return self._insert(cursor, category)

    def _insert(self, cursor, category: Category) -> Category:
        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_CATEGORY, NAME, ID_SUPER_CATEGORY)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            category.id_category,
            category.name,
            category.id_super_category,
        ))
        return category

    def _update(self, cursor, category: Category) -> Category:
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET NAME = %s, ID_SUPER_CATEGORY = %s
            WHERE ID_CATEGORY = %s;
        """
        cursor.execute(query, (
            category.name,
            category.id_super_category,
            category.id_category,
        ))
        return category

    def _exists(self, id_category: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID_CATEGORY FROM {self.TABLE_NAME} WHERE ID_CATEGORY = %s",
                    (id_category,),
                )
                return cursor.fetchone() is not None

    def find_by_id(self, id_value: str) -> Optional[Category]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ID_CATEGORY = %s",
                    (id_value,),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_all(self) -> List[Category]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                return [self._map_to_entity(row) for row in cursor.fetchall()]

    def delete(self, id_value: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE ID_CATEGORY = %s",
                    (id_value,),
                )
                return cursor.rowcount > 0

    def _map_to_entity(self, row) -> Category:
        return Category(
            id_category=row[0],
            name=row[1],
            id_super_category=row[2],
        )