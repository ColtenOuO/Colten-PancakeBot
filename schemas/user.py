from pydantic import BaseModel

from .item import Item

class User(BaseModel):
    user_id: int
    money: int = 0
    items: list[Item] = []
