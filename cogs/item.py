from pymongo import MongoClient
from datetime import datetime
from discord import ApplicationContext, Bot, Member, Embed
from discord.ext.commands import Cog, slash_command
from pymongo import MongoClient
from math import log10
from random import choice, randint, random, uniform
from stock.stock import StockSystem
from stock.stock1 import Stock1
import discord
from crud.user import CRUDUser
from schemas import User, UserUpdate
from database.database import DB
from cogs.fishing import Fishing
import json

with open('token.json') as f:
    tokens = json.load(f)
    client = MongoClient(tokens['db_client'])
class ItemCommands(Cog):
    bot: Bot
    crud_user: CRUDUser = CRUDUser()
    def __init__(self, bot):
        self.bot = bot
    @slash_command(name="item_pay",description="花費 20 個鬆餅使用一張還債卡，他可以讓你的負債歸 0")
    async def item_pay(self, ctx):
        DEFAULT = Fishing(self.bot)
        USER_DEFAULT_DATA = await DEFAULT.get_user(ctx.author.id)
        if( USER_DEFAULT_DATA.pancake < 20 ): await ctx.respond("你的鬆餅數量不足")
        else:
            if( USER_DEFAULT_DATA.money > 0 ): await ctx.respond("你明明就有錢，諧咖")
            elif( USER_DEFAULT_DATA.money == 0): await ctx.respond("你沒有負債但你也沒有錢，可撥")
            else:
                target_data = { 'discord_id': ctx.author.id }
                new_data = { '$set': { 'money': 0 } }
                client.pythondb['discord_user_data'].update_one(target_data,new_data)
                
                target_data = { 'discord_id': ctx.author.id }
                new_data = { '$set': { 'pancake': USER_DEFAULT_DATA.pancake - 20 } }
                client.pythondb['discord_user_data'].update_one(target_data,new_data)
                await ctx.respond("你使用了還債卡，讓你的負債歸 0 了！繼續努力，小心偷錢")


def setup(bot):
    bot.add_cog(ItemCommands(bot=bot))