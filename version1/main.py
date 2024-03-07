import discord
import random
from discord.ext import commands
import json
from fishing import fishing
from db import User, database

# Load tokens
with open('token.json') as f:
    tokens = json.load(f)

# Setup intents and bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", intents=intents)
token = tokens['tokens']
initial_extensions = ['slash_command.fishing','slash_command.item_command']

# Bot ready event
@bot.event
async def on_ready():
    db = database()
    print(">> Bot is online <<")



if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(token)
