from discord import Bot, Client
from discord.ext import tasks, commands
from stock.stock_information import information

from config import TOKEN

bot = Bot()
bot.load_extension("cogs.system")


@bot.event
async def on_ready():
    print(f"{bot.user.display_name} has connected to discord.")
    my_task.start()

@tasks.loop(minutes=20)  # 設置任務每 20 分鐘運行一次 
async def my_task():
    channel = bot.get_channel(1214270825075580990)  # 替換成目標頻道的 ID
    await channel.send(embed=information())

@my_task.before_loop
async def before_my_task():
    await bot.wait_until_ready()  # 等待機器人完全啟動

async def run():
    await bot.start(token=TOKEN)
