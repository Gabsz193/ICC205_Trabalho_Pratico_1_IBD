from typing import Optional

from pydantic import BaseModel


class Category(BaseModel):
    id_category: str
    name: Optional[str]
    id_super_category: Optional[str]