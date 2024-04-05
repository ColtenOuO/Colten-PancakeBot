from typing import Optional
from schemas import Billing, BillingUpdate
from .base import CRUDBase

class CRUDBilling(CRUDBase[Billing, BillingUpdate]):
    def __init__(self) -> None:
        super().__init__("billing_data", Billing)
    
    async def get_by_user_id(self, user_id: int) -> Optional[Billing]:
        result = await self.get(BillingUpdate(user_id=user_id))
        return result
    
    async def update_by_user_id(self, user_id: int, update: BillingUpdate) -> Optional[Billing]:
        result = await self.update(BillingUpdate(user_id=user_id), update)
        return result
    