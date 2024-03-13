from discord import (
    ApplicationContext,
    Bot,
    Embed,
    EmbedAuthor,
    EmbedFooter,
    Option,
    SlashCommandGroup
)

from asyncio import Task

from crud.stock import CRUDStock
from schemas import Stock, StockUpdate, UserUpdate

from .base import GroupCog, UserCog


class StockSystem(GroupCog, UserCog):
    bot: Bot
    crud_stock = CRUDStock()
    group = SlashCommandGroup(
        name="stock",
        description="Stock"
    )

    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def get_stock_code_list(self, *args) -> list[str]:
        return await self.crud_stock.get_all_code()

    @group.command(
        name="query",
        description="查詢股票",
        options=[
            Option(
                str,
                name="stock_code",
                description="股票代號",
                required=True,
                autocomplete=get_stock_code_list,
            )
        ]
    )
    async def query(
        self,
        ctx: ApplicationContext,
        stock_code: str
    ):
        stock = await self.crud_stock.get_by_code(stock_code)
        if stock is None:
            await ctx.respond("根本沒這個股票，搞什麼")
            return

        embed = Embed(
            color=stock.info.color,
            title=stock.info.title,
            url=stock.info.url,
            author=EmbedAuthor(
                name="目前股市"
            ),
            image=stock.info.image,
            thumbnail=stock.info.thumbnail,
            footer=EmbedFooter(
                text="美麗果民主共和國",
                icon_url="https://cdn.discordapp.com/icons/1180905078379520061/8433926f318fa5e118bd780a52603b54.webp"
            )
        )
        for field in stock.info.fields:
            embed.add_field(**field.model_dump())

        await ctx.respond(embed=embed)


def setup(bot: Bot):
    bot.add_cog(StockSystem(bot=bot))
