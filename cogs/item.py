from discord import ApplicationContext, Bot, SlashCommandGroup

from schemas import UserUpdate

from .base import GroupCog, UserCog


class ItemSystem(GroupCog, UserCog):
    bot: Bot
    group: SlashCommandGroup = SlashCommandGroup(
        name="item",
        description="Item"
    )

    def __init__(self, bot):
        self.bot = bot

    @group.command(
        name="pay_card",
        description="花費 20 個鬆餅使用一張還債卡，他可以讓你的負債歸 0"
    )
    async def pay_card(
        self,
        ctx: ApplicationContext
    ):
        user_id = ctx.author.id
        user = await self.get_user(user_id)

        if user.pancake < 20:
            await ctx.respond("你的鬆餅數量不足")
            return

        if user.money > 0:
            await ctx.respond("你明明就有錢，諧咖")
            return

        if user.money == 0:
            await ctx.respond("你沒有負債但你也沒有錢，可撥")
            return

        user_update = UserUpdate(
            money=0,
            pancake=user.pancake - 20
        )
        await self.crud_user.update_by_user_id(user_id, user_update)

        await ctx.respond("你使用了還債卡，讓你的負債歸 0 了！繼續努力，小心偷錢")


def setup(bot: Bot):
    bot.add_cog(ItemSystem(bot=bot))
