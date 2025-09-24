from pydantic import BaseModel


class Customer(BaseModel):
    id_customer: str
