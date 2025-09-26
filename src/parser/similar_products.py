from pydantic import BaseModel


class SimilarProducts(BaseModel):
    id_product: str
    id_similar_product: str
    rank: int