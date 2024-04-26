from discord import Bot

from asyncio import get_event_loop, sleep as asleep

from config import MAIN_CHANNEL, TOKEN
from stock.update import update_stocks

bot = Bot()
init = False

async def broadcast_buy(stock_name: str,stock_code: str, stock_amount: int, stock_price: int):
    channel = bot.get_channel(MAIN_CHANNEL)
    await channel.send(f'委託成功！買進股票名稱：{stock_name}，委託買進價格 {stock_price}')
    

async def broadcast_stock():
    while True:
        await bot.wait_until_ready()
        channel = bot.get_channel(MAIN_CHANNEL)
        embeds = await update_stocks()
        #if len(embeds) > 0:
            #await channel.send(embeds=embeds)
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
