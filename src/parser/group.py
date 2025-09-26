from typing import Optional

from pydantic import BaseModel


class Group(BaseModel):
    id_group: str
    name: Optional[str]
