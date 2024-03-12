from typing import Optional

from schemas import Bank, BankUpdate

from .base import CRUDBase


class CRUDBank(CRUDBase[Bank, BankUpdate]):
    def __init__(self) -> None:
        super().__init__("bank_data", Bank)

    async def get_by_user_id(self, user_id: int) -> Optional[Bank]:
        result = await self.get(BankUpdate(user_id=user_id))

        return result

    async def update_by_user_id(self, user_id: int, update: BankUpdate) -> Optional[Bank]:
        result = await self.update(BankUpdate(user_id=user_id), update)

        return result
