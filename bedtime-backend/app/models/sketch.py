# app/models/item.py
from pydantic import BaseModel

class sketch(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
