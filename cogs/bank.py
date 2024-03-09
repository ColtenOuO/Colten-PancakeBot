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

class BankSystem(Cog):
    bot: Bot
    crud_user: CRUDUser = CRUDUser()
    stock_system: StockSystem = StockSystem()
    stock1: Stock1 = Stock1()

    def __init__(self, bot):
        self.bot = bot
    def get_user(self,discord_id: int):
        for USER in client.pythondb["bank_data"].find():
            if( USER["discord_id"] == discord_id ): return USER
        return None
    def new_user(self,discord_id: int):
        new_user = {
            "discord_id": discord_id,
            "BANK_MONEY": 0,
            "MAX_MONEY": 1000,
            "STOCK": []
        }
        client.pythondb["bank_data"].insert_one(new_user)
    @slash_command(name="bank",description="查詢你的銀行目前有多少錢 (銀行內的錢不會被偷走)")
    async def bank(self, ctx: ApplicationContext):
        USER_DATA = self.get_user(discord_id=ctx.author.id)
        if( USER_DATA == None ): await ctx.respond("你的銀行內目前前有 0/1000 元")
        else: await ctx.respond(f"你目前銀行內有 {USER_DATA['BANK_MONEY']}/{USER_DATA['MAX_MONEY']} 元")
    
    @slash_command(name="save_money",description="將你的錢存入銀行")
    async def save_money(self, ctx: ApplicationContext, input_money: int):
        DEFAULT = Fishing(self.bot)
        if( self.get_user(discord_id=ctx.author.id) == None ): self.new_user(ctx.author.id)
        USER_BANK_DATA = self.get_user(discord_id=ctx.author.id)
        USER_DEFAULT_DATA = await DEFAULT.get_user(ctx.author.id)
        print(type(USER_DEFAULT_DATA))
        
        remain = USER_BANK_DATA['MAX_MONEY'] - USER_BANK_DATA['BANK_MONEY']
        
        if( USER_DEFAULT_DATA.money < 0 ): await ctx.respond("你他媽負債還想存錢？？？")
        elif( USER_DEFAULT_DATA.money < input_money ): await ctx.respond("你的錢根本沒有這麼多，搞什麼")
        elif( input_money > remain ): await ctx.respond(f"你的銀行沒辦法存入這麼多錢，你最多只能再存 {remain} 元")
        else:
            user_update = UserUpdate(money=USER_DEFAULT_DATA['money'] + input_money)
            await self.crud_user.update_by_user_id(ctx.author.id, user_update)

            target_data = { 'discord_id': ctx.author.id }
            new_data = { '$set': { 'BANK_MONEY': USER_BANK_DATA['BANK_MONEY'] + input_money } }
            client.pythondb['bank_data'].update_one(target_data,new_data)
            await ctx.respond(f"存錢成功！你的銀行內目前有 {USER_BANK_DATA['BANK_MONEY'] + input_money} 元")

            # 扣錢
            user_update = UserUpdate(money = USER_DEFAULT_DATA.money - input_money)
            await self.crud_user.update_by_user_id(ctx.author.id, user_update)

    @slash_command(name="stock_query",description="查詢目前股市")
    async def stock_query(self, ctx: ApplicationContext):
        await ctx.respond("查詢中...")
        await ctx.send(embed=self.stock1.get_information())

    

def setup(bot: Bot):
    bot.add_cog(BankSystem(bot=bot))
        

