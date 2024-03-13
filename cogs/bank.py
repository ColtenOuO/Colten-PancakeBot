from discord import ApplicationContext, Bot, SlashCommandGroup

from crud.bank import CRUDBank
from schemas import Bank, BankUpdate, UserUpdate

from .base import GroupCog, UserCog


class BankSystem(GroupCog, UserCog):
    bot: Bot
    crud_bank = CRUDBank()
    group = SlashCommandGroup(
        name="bank",
        description="Bank operation"
    )

    async def get_bank(self, user_id: int) -> Bank:
        bank = await self.crud_bank.get_by_user_id(user_id)
        if bank is None:
            bank = await self.crud_bank.create(Bank(user_id=user_id))
        return bank

    @group.command(
        name="query",
        description="查詢你的銀行目前有多少錢 (銀行內的錢不會被偷走)"
    )
    async def query(
        self,
        ctx: ApplicationContext
    ):
        bank = await self.get_bank(ctx.author.id)
        await ctx.respond(f"你目前銀行內有 {bank.money}/{bank.max_money} 元")

    @group.command(
        name="save",
        description="將你的錢存入銀行"
    )
    async def save(
        self,
        ctx: ApplicationContext,
        save_money: int
    ):
        user_id = ctx.author.id
        user = await self.get_user(user_id)
        bank = await self.get_bank(user_id)

        remain_space = bank.max_money - bank.money

        if user.money < 0:
            await ctx.respond("你他媽負債還想存錢？？？")
            return

        if user.money < save_money:
            await ctx.respond("你的錢根本沒有這麼多，搞什麼")
            return

        if save_money > remain_space:
            await ctx.respond(f"你的銀行沒辦法存入這麼多錢，你最多只能再存 {remain_space} 元")
            return

        bank_update = BankUpdate(
            money=bank.money + save_money
        )
        bank = await self.crud_bank.update_by_user_id(user_id, bank_update)

        user_update = UserUpdate(
            money=user.money - save_money
        )
        await self.crud_user.update_by_user_id(user_id, user_update)

        await ctx.respond(f"存錢成功！你的銀行內目前有 {bank.money} 元")

    @group.command(
        name="take",
        description="提款"
    )
    async def take(
        self,
        ctx: ApplicationContext,
        take_money: int
    ):
        user_id = ctx.author.id
        user = await self.get_user(user_id)
        bank = await self.get_bank(user_id)

        if bank.money < take_money:
            await ctx.respond("你銀行裡的錢根本沒有這麼多，搞什麼")
            return

        bank_update = BankUpdate(
            money=bank.money - take_money
        )
        bank = await self.crud_bank.update_by_user_id(user_id, bank_update)

        user_update = UserUpdate(
            money=user.money + take_money
        )
        await self.crud_user.update_by_user_id(ctx.author.id, user_update)

        await ctx.respond(f"提款成功！你的銀行內目前還有 {bank.money} 元")


def setup(bot: Bot):
    bot.add_cog(BankSystem(bot=bot))
