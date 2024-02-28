from discord import Bot, Client

from config import TOKEN

bot = Bot()

async def run():
    await bot.start(token=TOKEN)
