from discord import Bot, SlashCommandGroup
from discord.ext.commands import Cog

from typing import Optional

from crud.user import CRUDUser
from schemas import User


class GroupCog(Cog):
    bot: Optional[Bot] = None
    group: Optional[SlashCommandGroup] = None

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    def cog_unload(self) -> None:
        if self.group is not None:
            self.bot.remove_application_command(self.group)
        return super().cog_unload()


class UserCog(Cog):
    crud_user: CRUDUser = CRUDUser()

    async def get_user(self, user_id: int) -> User:
        user = await self.crud_user.get_by_user_id(user_id)
        if user is None:
            user = await self.crud_user.create(User(user_id=user_id))
        return user
