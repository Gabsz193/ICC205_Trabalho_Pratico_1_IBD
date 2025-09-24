from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel

class Group(BaseModel):
    name: str

class Category(BaseModel):
    id_category: str
    name: str
    super_category: Optional['Category'] = None

class SimilarProduct(BaseModel):
    id_similar_product: str

class Customer(BaseModel):
    id_customer: str

class Review(BaseModel):
    customer: Customer
    dt_review: datetime
    rating: Literal[1, 2, 3, 4, 5]
    qtd_votes: int
    qtd_helpful_votes: int

class Product(BaseModel):
    id_product: str
    asin: str
    title: Optional[str] = None
    group: Optional[Group] = None
    categories: list[Category] = []
    similarProducts: list[SimilarProduct] = []
    reviews: list[Review] = []
    avg_rating: Optional[float] = None
    total_downloaded: Optional[int] = None
    salesrank: Optional[int] = None