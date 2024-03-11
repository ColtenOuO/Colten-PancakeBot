from discord import Bot
from discord.ext import tasks
from stock.stock_information import information
from config import TOKEN

bot = Bot()
bot.load_extension("cogs.system")

# Assuming TOKEN and other necessary imports are defined elsewhere in your code.

# Global variable to keep track of the task's state
my_task_started = False

@tasks.loop(minutes=10)
async def my_task():
    channel = bot.get_channel(1214270825075580990)  # Replace with your target channel ID
    await channel.send(embed=information())

@bot.event
async def on_ready():
    print(f"{bot.user.display_name} has connected to Discord.")
    global my_task_started
    if not my_task_started:
        my_task.start()
        my_task_started = True  # Mark the task as started

async def run():
    await bot.start(TOKEN)

# Assuming the run() function is called appropriately elsewhere in your code.
