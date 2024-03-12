from pydantic import BaseModel

from typing import Optional


class Bank(BaseModel):
    user_id: int
    money: int = 0
    max_money: int = 1000


class BankUpdate(BaseModel):
    user_id: Optional[int] = None
    money: Optional[int] = None
    max_money: Optional[int] = None
