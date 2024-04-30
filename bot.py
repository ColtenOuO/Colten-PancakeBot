from discord import Bot

from asyncio import get_event_loop, sleep as asleep

from config import MAIN_CHANNEL, TOKEN, STCOK_CHANNEL
from stock.update import update_stocks

bot = Bot()
init = False

async def broadcast_buy(discord_id: int, stock_name: str,stock_code: str, stock_amount: int, stock_price: int):
    channel = bot.get_channel(STCOK_CHANNEL)
    await channel.send(f'【委託買進單】<@{discord_id}> 委託買進股票：{stock_name} 共 {stock_amount} 股，委託買進價格 {stock_price} / 1 股')
async def broadcast_sell(discord_id: int, stock_name: str,stock_code: str, stock_amount: int, stock_price: int):
    channel = bot.get_channel(STCOK_CHANNEL)
    await channel.send(f'【委託賣出單】<@{discord_id}> 委託賣出股票：{stock_name} 共 {stock_amount} 股，委託賣出價格 {stock_price} / 1 股')
async def broadcast_match(buy_id: int, sell_id:int, stock_name: str, stock_code: str, stock_amount: int, stock_price: int):
    channel = bot.get_channel(STCOK_CHANNEL)
    await channel.send(f'【買進成交】<@{buy_id}> 委託買進 {stock_code} 共 {stock_amount} 股，委託買進價格 {stock_price}，已全數成交')
    await channel.send(f'【賣出成交】<@{sell_id}> 委託賣出 {stock_code} 共 {stock_amount} 股，委託賣出價格 {stock_price}，已全數成交')


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
