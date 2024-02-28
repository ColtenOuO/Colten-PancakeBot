from discord import Bot, SlashCommandGroup
from discord.ext.commands import Cog

from typing import Optional

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
