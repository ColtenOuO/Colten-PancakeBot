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

fishing_instance = fishing()  # Renamed variable to avoid naming conflict
db = database()

# Bot ready event
@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.slash_command(name="fishing",description="釣起一隻魚，目前釣起高睿的機率為 1/90 !")
async def fishing_cmd(ctx):  # Renamed function to avoid naming conflict
    fish_result = fishing_instance.fishing()
    cm = round(random.uniform(0, 1000))
    dv = round(random.uniform(1, 200))
    
    if( db.Register_Query(ctx.author.id) == False ): db.Registered(ctx.author.id)
    get_money: int
    get_money = int(cm / dv)
    
    await ctx.respond(f"你釣起了一隻 {cm} cm 的 {fish_result} 獲得了 {get_money} 元")
    adding_money = db.update_user(get_money,0)
    adding_money.update_money(db,ctx.author.id,adding_money)

@bot.slash_command(name="money",description="查詢自己有多少錢")
async def fishing_cmd(ctx):  # Renamed function to avoid naming conflict 
    ans = db.Register_Query(ctx.author.id)
    if( ans == False ): await ctx.respond("你目前有 0 元，哈哈")
    else: await ctx.respond(f"你目前有 {db.User_Query(ctx.author.id)["money"]} 元！")



# Run the bot
bot.run(token)
