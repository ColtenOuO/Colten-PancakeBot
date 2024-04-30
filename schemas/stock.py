from pydantic import BaseModel

from typing import Optional

from .discord import EmbedField

class StockInfo(BaseModel):
    title: str = ""
    url: Optional[str] = None
    image: Optional[str] = None
    thumbnail: Optional[str] = None
    color: int = 0x00b0f4
    fields: list[EmbedField] = []


class Stock(BaseModel):
    code: str = ""
    price: int = 1000
    delta: int = 0
    remain: int = 10000
    info: StockInfo = StockInfo()


class StockUpdate(BaseModel):
    code: Optional[str] = None
    price: Optional[int] = None
    delta: Optional[int] = None                             

class StockOrder(BaseModel):
    discord_id: Optional[int] = None
    code: Optional[int] = None
    price: Optional[int] = None
