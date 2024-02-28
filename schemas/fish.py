from pydantic import BaseModel

class Fish(BaseModel):
    fish_id = int
    display_name: str
    size: float
    price: int
