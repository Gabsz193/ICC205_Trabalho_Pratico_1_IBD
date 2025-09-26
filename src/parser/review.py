from datetime import datetime

from pydantic import BaseModel


class Review(BaseModel):
    id_review: str
    id_product: str
    id_customer: str
    dt_review: datetime
    rating: int
    qtd_votes: int
    qtd_helpful_votes: int