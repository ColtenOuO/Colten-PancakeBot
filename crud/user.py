from typing import Optional

from schemas import User, UserUpdate

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserUpdate]):
    def __init__(self) -> None:
        super().__init__("discord_user_data", User)

    async def get_by_user_id(self, user_id: int) -> Optional[User]:
        result = await self.get(UserUpdate(user_id=user_id))

        return result

    async def update_by_user_id(self, user_id: int, update: UserUpdate) -> Optional[User]:
        result = await self.update(UserUpdate(user_id=user_id), update)

        return result
