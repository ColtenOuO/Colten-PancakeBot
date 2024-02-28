from pydantic import BaseModel

class Item(BaseModel):
    item_id: int
    display_name: str
    price: int
    count: int = 0
