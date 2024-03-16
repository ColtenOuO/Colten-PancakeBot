from asyncio import create_task, run, gather

from bot import run as bot_run
from stock_web.backend import start_api

DEBUG = False


async def main():
    if DEBUG:
        from crud.stock import CRUDStock
        from schemas import EmbedField, Stock
        from schemas.stock import StockInfo
        crud_stock = CRUDStock()
        if await crud_stock.get_by_code("gray") is None:
            stack_info = StockInfo(
                title="高睿屬實有料股份有限公司",
                url="https://joeshih.com/portfolio/國立成功大學敬業校區學生宿舍",
                image="https://manage-oga.ncku.edu.tw/var/file/189/1189/img/Livingroom-Salon.jpg",
                thumbnail="https://pic.pimg.tw/sobeit/114268963199_n.jpg",
                color=0x00b0f4,
                fields=[
                    EmbedField(
                        name="公司登記地址",
                        value="國立成功大學敬業校區第一宿舍 209 號房",
                        inline=False
                    ),
                    EmbedField(
                        name="公司介紹",
                        value="高睿屬實有料股份有限公司成立於 2024 年 3 月，主要以發展睡眠產業為主，旗下開發的產品多數廣受市場的好評，並讓許多客戶滿意到常常說出『屬實有料』一詞而聞名。",
                        inline=False
                    ),
                    EmbedField(
                        name="公司資本額",
                        value="1000 萬元",
                        inline=True
                    ),
                    EmbedField(
                        name="公司負責人",
                        value="高睿",
                        inline=True
                    )
                ]
            )
            stock = Stock(
                code="gray", info=stack_info
            )
            await crud_stock.create(stock)

    await gather(
        create_task(bot_run()),
        create_task(start_api()),
    )

if __name__ == "__main__":
    run(main=main())
