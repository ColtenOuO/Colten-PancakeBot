from discord import Embed

from asyncio import gather
from random import randint

from crud.stock import CRUDStock
from schemas import EmbedField, StockUpdate

crud_stock = CRUDStock()


async def update_stocks() -> list[Embed]:
    results = []
    offset = 0
    while True:
        code_list = await crud_stock.get_all_code(
            offset=offset,
            limit=25
        )
        if len(code_list) == 0:
            break

        async def modify(stock_code: str) -> EmbedField:
            stock = await crud_stock.get_by_code(stock_code)
            new_delta = stock.delta + randint(-100, 100)
            new_price = stock.price + new_delta

            stock_update = StockUpdate(
                price=new_price,
                delta=new_delta
            )
            await crud_stock.update_by_code(stock_code, stock_update)

            return EmbedField(
                name=stock.info.title,
                value=f"目前股市狀況 (1 股價格): {new_price} 元 (價格變動: {'+' if new_delta > 0 else ''}{new_delta})",
                inline=False
            )

        embed_fields = await gather(*list(map(modify, code_list)))

        embed = Embed(
            title="今日股市變動！！！",
            description="投資一定有風險，基金投資有賺有賠，申購前應詳閱公開說明書",
            image="https://stickershop.line-scdn.net/stickershop/v1/product/6287/LINEStorePC/main.png?v=1",
            thumbnail="https://down-tw.img.susercontent.com/file/22b1fc845e5ce92481d08c79ffa29296",
        )
        for field in embed_fields:
            embed.add_field(**field.model_dump())
        results.append(embed)

        if len(code_list) < 25:
            break
        offset += 25
    return results
