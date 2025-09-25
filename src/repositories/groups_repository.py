from typing import Optional, List

from models.group import Group
from repositories.base import BaseRepository


class GroupRepository(BaseRepository[Group]):
    TABLE_NAME: str = "Groups"

    def save(self, group: Group) -> Group:
        with self.connection as conn:
            with conn.cursor() as cursor:
                if self._exists(group.id_group):
                    return self._update(cursor, group)
                else:
                    return self._insert(cursor, group)

    def _insert(self, cursor, group: Group) -> Group:
        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_GROUP, NAME)
            VALUES (%s, %s)
        """
        cursor.execute(query, (
            group.id_group,
            group.name,
        ))
        return group

    def _update(self, cursor, group: Group) -> Group:
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET NAME = %s
            WHERE ID_GROUP = %s;
        """
        cursor.execute(query, (
            group.name,
            group.id_group,
        ))
        return group

    def _exists(self, id_group: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID_GROUP FROM {self.TABLE_NAME} WHERE ID_GROUP = %s",
                    (id_group,),
                )
                return cursor.fetchone() is not None

    def find_by_id(self, id_value: str) -> Optional[Group]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ID_GROUP = %s",
                    (id_value,),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_all(self) -> List[Group]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                return [self._map_to_entity(row) for row in cursor.fetchall()]

    def delete(self, id_value: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE ID_GROUP = %s",
                    (id_value,),
                )
                return cursor.rowcount > 0

    def _map_to_entity(self, row) -> Group:
        return Group(
            id_group=row[0],
            name=row[1],
        )