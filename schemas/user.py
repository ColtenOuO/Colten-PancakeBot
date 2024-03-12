from pydantic import BaseModel

from typing import Optional


class User(BaseModel):
    user_id: int
    money: int = 0
    pancake: int = 0
    experience: int = 0
    stock: dict[str, int] = {}


class UserUpdate(BaseModel):
    user_id: Optional[int] = None
    money: Optional[int] = None
    pancake: Optional[int] = None
    experience: Optional[int] = None
    stock: Optional[dict[str, int]] = None
