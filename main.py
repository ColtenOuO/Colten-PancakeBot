import discord
import random
import time
from discord.ext import commands
from init import init, fishing
import json

# Load tokens
with open('token.json') as f:
    tokens = json.load(f)

# Setup intents and bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", intents=intents)
token = tokens['tokens']

# Initialize any necessary components
init()

# Bot ready event
@bot.event
async def on_ready():
    print(">> Bot is online <<")

# Test slash command
@bot.slash_command(name="test")
async def first_slash(ctx):
    await ctx.respond("Hello world")

# Fishing slash command
@bot.slash_command(name="fishing")
async def second_slash(ctx):
    fish = fishing()
    cm = round(random.uniform(0,1000))
    # Corrected string formatting
    await ctx.respond(f"你釣起了一隻 {cm} cm 的 {fish} 獲得了 {cm/10} 元")

# Run the bot
bot.run(token)
