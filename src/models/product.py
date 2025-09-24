from typing import Optional

from pydantic import BaseModel

class Product(BaseModel):
    id_product: str
    asin: str
    title: Optional[str]
    id_group: Optional[str]
    salesrank: Optional[int]
    total: Optional[int]
    avg_rating: Optional[float]