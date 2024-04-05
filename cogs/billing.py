from discord import (
    ApplicationContext,
    Bot,
    SlashCommandGroup,
    Member
)
from discord.ext.commands import Cog
from crud.billing import CRUDBilling
from schemas import Billing, BillingUpdate


class BillingSystem(Cog):
    bot: Bot
    group = SlashCommandGroup(
        name="billing",
        description="Billing"
    )
    crud_billing = CRUDBilling()
    def __init__(self, bot) -> None:
        self.bot = bot
    
    async def add(self, user: Member, money: int):
        info = await self.crud_billing.get_by_user_id(user.id)
        result = 0
        if info == None:
            result = money
            await self.crud_billing.create(Billing(user_id=user.id, name=user.display_name, money=money))
        else:
            result = info.money + money
            update = BillingUpdate(money=result)
            await self.crud_billing.update_by_user_id(user.id, update)
        return result

    @group.command()
    async def begging(self, ctx: ApplicationContext, money: int, opponent: Member):
        if money < 0:
            await ctx.respond(f"錢是負的")
            return
        info = await self.crud_billing.get_by_user_id(ctx.author.id)
        if info != None and info.money <= -500:
            result = info.money
            await ctx.respond(f"你已經欠{-result}了還想乞討阿，快還錢吧乞丐")
            return

        if ctx.author.display_name == opponent.display_name:
            await ctx.respond(f"自己向自己乞求幹嘛，你也太可憐了吧")
            return
        if opponent.display_name == self.bot.user.display_name:
            await ctx.respond(f"向機器人乞討幹嘛，乞丐")
            return
        result1 = await self.add(ctx.author, -money)
        result2 = await self.add(opponent, money)
        await ctx.respond(f"可憐的{ctx.author.mention}向{opponent.mention}乞求了{money}元\n{ctx.author.display_name}現在有{result1}元\n{opponent.display_name}現在有{result2}元")


    @group.command()
    async def paying(self, ctx: ApplicationContext, money: int, opponent: Member):
        if money < 0:
            await ctx.respond(f"錢是負的")
            return
        if ctx.author.display_name == opponent.display_name:
            await ctx.respond(f"自己付自己錢幹嘛")
            return
        if opponent.display_name == self.bot.user.display_name:
            await ctx.respond(f"付機器人錢幹嘛，凱子")
            return
        result1 = await self.add(ctx.author, money)
        result2 = await self.add(opponent, -money)
        await ctx.respond(f"{ctx.author.mention}向{opponent.mention}支付了{money}元\n{ctx.author.display_name}現在有{result1}元\n{opponent.display_name}現在有{result2}元")

    @group.command()
    async def query(self, ctx: ApplicationContext):
        people = await self.crud_billing.get_many(dict({}), 0)
        people.sort(key=lambda person: -person.money)
        result = ""
        for person in people:
            name = person.name
            money = person.money
            result += f"{name}有{money}元\n"
        await ctx.respond(result)
def setup(bot: Bot):
    bot.add_cog(BillingSystem(bot=bot))