import discord
import random
from discord.ext import commands
import json
from fishing import fishing

# Load tokens
with open('token.json') as f:
    tokens = json.load(f)

# Setup intents and bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", intents=intents)
token = tokens['tokens']

fishing_instance = fishing()  # Renamed variable to avoid naming conflict

# Bot ready event
@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.slash_command(name="fishing")
async def fishing_cmd(ctx):  # Renamed function to avoid naming conflict
    fish_result = fishing_instance.fishing()
    cm = round(random.uniform(0, 1000))
    await ctx.respond(f"你釣起了一隻 {cm} cm 的 {fish_result} 獲得了 {cm/10} 元")

# Run the bot
bot.run(token)
