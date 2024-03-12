from discord import Bot

from asyncio import get_event_loop, sleep as asleep

from config import MAIN_CHANNEL, TOKEN
from stock.update import update_stocks

bot = Bot()
bot.load_extension("cogs.system")

init = False

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
        loop = get_event_loop()
        loop.create_task(broadcast_stock())


async def run():
    await bot.start(TOKEN)
