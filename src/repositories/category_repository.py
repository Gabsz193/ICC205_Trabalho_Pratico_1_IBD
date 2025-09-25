from typing import Optional, List, Union

from models.category import Category
from repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    TABLE_NAME: str = "Category"

    def save(self, entity: Union[Category, List[Category]]) -> Union[Category, List[Category]]:
        if isinstance(entity, list):
            with self.connection as conn:
                with conn.cursor() as cursor:
                    return self._insert_all(cursor, entity)
        else:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    if self._exists(entity.id_category):
                        return self._update(cursor, entity)
                    else:
                        return self._insert(cursor, entity)

    def _insert_all(self, cursor, categories: List[Category]) -> List[Category]:
        categories_checkeck = set()
        unicos = []

        categories = [category.model_dump() for category in categories if category is not None]

        for category in categories:
            if category['id_category'] not in categories_checkeck:
                categories_checkeck.add(category['id_category'])
                unicos.append(category)

        categories = [unico for unico in unicos if not self._exists(unico['id_category'])]

        if not categories:
            return []

        placeholders = ','.join(['(%s, %s, %s)' for _ in categories])

        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_CATEGORY, NAME, ID_SUPER_CATEGORY)
            VALUES {placeholders}
        """



        params = []
        for p in categories:
            params.extend([
                p['id_category'],
                p['name'],
                p['id_super_category'],
            ])

        cursor.execute(query, tuple(params))

        return categories

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
