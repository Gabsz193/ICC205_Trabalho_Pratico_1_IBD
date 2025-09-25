from enum import unique
from typing import Optional, List, Union

from models.group import Group
from repositories.base import BaseRepository


class GroupRepository(BaseRepository[Group]):
    TABLE_NAME: str = "Groups"

    def save(self, entity: Union[Group, List[Group]]) -> Union[Group, List[Group]]:
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

    def _insert_all(self, cursor, groups: List[Group]) -> List[Group]:

        groups_checkeck = set()
        unicos = []

        groups = [group.model_dump() for group in groups if group is not None]

        for group in groups:
            if group['id_group'] not in groups_checkeck:
                groups_checkeck.add(group['id_group'])
                unicos.append(group)

        groups = [unico for unico in unicos if not self._exists(unico['id_group'])]

        if not groups:
            return []

        placeholders = ','.join(['(%s, %s)' for _ in groups])

        query = f"""
            INSERT INTO {self.TABLE_NAME} (ID_GROUP, NAME)
            VALUES {placeholders}
        """
        params = []

        for p in groups:
            # garantir a ordem correta dos campos
            params.extend([
                p['id_group'],
                p['name']
            ])
        cursor.execute(query, tuple(params))

        return groups

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

    def _exists(self, name: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT NAME FROM {self.TABLE_NAME} WHERE NAME = %s",
                    (name,),
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
