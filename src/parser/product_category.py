from pydantic import BaseModel


class ProductCategory(BaseModel):
    id_product_category: str
    id_product: str
    id_category: str