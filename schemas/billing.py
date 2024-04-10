from pydantic import BaseModel
from typing import Optional

class Billing(BaseModel):
    user_id: int
    name: str
    money: int = 0

class BillingUpdate(BaseModel):
    user_id: Optional[int] = None
    name: Optional[str] = None
    money: Optional[int] = 0