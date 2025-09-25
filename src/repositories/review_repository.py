from typing import Optional, List, Union
from datetime import datetime

from models.review import Review
from repositories.base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    TABLE_NAME: str = "Review"

    def save(self, entity: Union[Review, List[Review]]) -> Union[Review, List[Review]]:
        if isinstance(entity, list):
            with self.connection as conn:
                with conn.cursor() as cursor:
                    return self._insert_all(cursor, entity)
        else:
            with self.connection as conn:
                with conn.cursor() as cursor:
                    if self._exists(entity.id_review):
                        return self._update(cursor, entity)
                    else:
                        return self._insert(cursor, entity)

    def _insert_all(self, cursor, reviews: List[Review]) -> List[Review]:
        placeholders = ','.join(['(%s, %s, %s, %s, %s, %s, %s)' for _ in reviews])

        query = f"""
                    INSERT INTO {self.TABLE_NAME} (ID_REVIEW, ID_PRODUCT, ID_CUSTOMER, DT_REVIEW, RATING, QTD_VOTES, QTD_HELPFUL_VOTES)
                    VALUES {placeholders}
                """
        params = []

        for p in reviews:
            # garantir a ordem correta dos campos
            params.extend([
                p.id_review,
                p.id_product,
                p.id_customer,
                p.dt_review,
                p.rating,
                p.qtd_votes,
                p.qtd_helpful_votes,
            ])
        cursor.execute(query, tuple(params))

        return reviews

    def _insert(self, cursor, review: Review) -> Review:
        query = f"""
            INSERT INTO {self.TABLE_NAME} 
            (ID_REVIEW, ID_PRODUCT, ID_CUSTOMER, DT_REVIEW, RATING, QTD_VOTES, QTD_HELPFUL_VOTES)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            review.id_review,
            review.id_product,
            review.id_customer,
            review.dt_review,
            review.rating,
            review.qtd_votes,
            review.qtd_helpful_votes,
        ))
        return review

    def _update(self, cursor, review: Review) -> Review:
        query = f"""
            UPDATE {self.TABLE_NAME}
            SET ID_PRODUCT = %s, ID_CUSTOMER = %s, DT_REVIEW = %s, RATING = %s, 
                QTD_VOTES = %s, QTD_HELPFUL_VOTES = %s
            WHERE ID_REVIEW = %s;
        """
        cursor.execute(query, (
            review.id_product,
            review.id_customer,
            review.dt_review,
            review.rating,
            review.qtd_votes,
            review.qtd_helpful_votes,
            review.id_review,
        ))
        return review

    def _exists(self, id_review: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT ID_REVIEW FROM {self.TABLE_NAME} WHERE ID_REVIEW = %s",
                    (id_review,),
                )
                return cursor.fetchone() is not None

    def find_by_id(self, id_value: str) -> Optional[Review]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE ID_REVIEW = %s",
                    (id_value,),
                )
                row = cursor.fetchone()
                if row:
                    return self._map_to_entity(row)
                return None

    def find_all(self) -> List[Review]:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                return [self._map_to_entity(row) for row in cursor.fetchall()]

    def delete(self, id_value: str) -> bool:
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE ID_REVIEW = %s",
                    (id_value,),
                )
                return cursor.rowcount > 0

    def _map_to_entity(self, row) -> Review:
        return Review(
            id_review=row[0],
            id_product=row[1],
            id_customer=row[2],
            dt_review=row[3],
            rating=row[4],
            qtd_votes=row[5],
            qtd_helpful_votes=row[6],
        )