from discord import Bot

from asyncio import get_event_loop, sleep as asleep

from config import MAIN_CHANNEL, TOKEN
from stock.update import update_stocks

bot = Bot()
init = False

async def broadcast_stock(stock_price: int,stock_count: int):
    channel = bot.get_channel(1214270825075580990)
    await channel.send(f'剛剛 Colten 用 {stock_price} 的價格買入了 {stock_price} 股「玻璃質量測試股份有限公司」的股份')
async def broadcast_stock():
    while True:
        await bot.wait_until_ready()
        channel = bot.get_channel(MAIN_CHANNEL)
        embeds = await update_stocks()
        if len(embeds) > 0:
            await channel.send(embeds=embeds)
        await asleep(600)


@bot.event
async def on_ready():
    global init
    print(f"{bot.user.display_name} has connected to Discord.")

    if not init:
        init = True
        loop = bot.loop
        loop.create_task(broadcast_stock())


async def run():
    bot.loop = get_event_loop()
    bot.load_extension("cogs.system")
    await bot.start(TOKEN)
