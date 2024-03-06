from discord import Bot, Client

from config import TOKEN

bot = Bot()
bot.load_extension("cogs.system")


@bot.event
async def on_ready():
    print(f"{bot.user.display_name} has connected to discord.")


async def run():
    await bot.start(token=TOKEN)
