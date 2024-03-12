from discord import (
    ApplicationContext,
    Bot,
    Embed,
    EmbedAuthor,
    EmbedFooter,
    Option,
    SlashCommandGroup
)

from asyncio import run
from typing import Annotated

from crud.stock import CRUDStock
from schemas import Stock, StockUpdate, UserUpdate

from .base import GroupCog, UserCog

import time
from crud.mining import MiningData



class MiningSystem(GroupCog, UserCog):
    bot: Bot
    crud_mining: MiningData = MiningData()
    def __init__(self,bot) -> None:
        self.bot = bot
    group: SlashCommandGroup = SlashCommandGroup(
        name="mining",
        description="Mining"
    )
    @group.command(name="start",description="開始挖礦 (20 分鐘後可以回來收集結果)")
    async def mining(self,ctx):
        USER_DATA = self.crud_mining.query_user(ctx.author.id)
        if( USER_DATA != None and USER_DATA['last_time'] != None  ): await ctx.respond("你已經在挖礦了啦，搞什麼")
        else:
            if( USER_DATA == None ): self.crud_mining.insert_new_one(ctx.author.id,None)
            self.crud_mining.update_one(discord_id=ctx.author.id,user_time=time.time())
            await ctx.respond("開始挖礦！20 分鐘後可以回來領取獎勵 ><")
        
def setup(bot: Bot):
    bot.add_cog(MiningSystem(bot=bot))
    
    