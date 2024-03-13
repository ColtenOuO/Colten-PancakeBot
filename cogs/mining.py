from discord import (
    ApplicationContext,
    Bot,
    SlashCommandGroup
)

from datetime import datetime
from math import log

from schemas import UserUpdate

from .base import GroupCog, UserCog


class MiningSystem(GroupCog, UserCog):
    bot: Bot
    group = SlashCommandGroup(
        name="mining",
        description="Mining"
    )

    def __init__(self, bot) -> None:
        self.bot = bot

    @group.command(
        name="start",
        description="開始挖礦 (20 分鐘後可以回來收集結果)"
    )
    async def start_mining(self, ctx: ApplicationContext):
        user_id = ctx.author.id
        user = await self.get_user(user_id)

        if user.mining_time != 0:
            await ctx.respond("你已經在挖礦了啦，搞什麼")
            return

        user_update = UserUpdate(
            mining_time=int(datetime.utcnow().timestamp())
        )
        await self.crud_user.update_by_user_id(user_id, user_update)

        await ctx.respond("開始挖礦！ 20 分鐘後可以回來領取獎勵 ><")

    @group.command(
        name="stop",
        description="停止挖礦"
    )
    async def stop_mining(self, ctx: ApplicationContext):
        user_id = ctx.author.id
        user = await self.get_user(user_id)

        if (user.mining_time == 0):
            await ctx.respond("你根本沒有在挖礦，搞什麼")
            return
        
        user_update = UserUpdate(
            mining_time=0
        )
        await self.crud_user.update_by_user_id(user_id, user_update)

        base_money = 1000

        delta_time = (datetime.utcnow().timestamp() - user.mining_time) / 1200
        get_money = int(log(delta_time) * base_money)

        if get_money < 0:
            await ctx.respond(f"根本就還沒到20分鐘，搞什麼，你罰 {get_money} 元")
            return
        
        get_money += base_money
        await ctx.respond(f"你挖了 {int(delta_time * 20)} 分鐘 獲得 {get_money} 元")


def setup(bot: Bot):
    bot.add_cog(MiningSystem(bot=bot))
