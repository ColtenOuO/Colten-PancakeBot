import discord
from discord.ext import commands
from db import database
from item.item_db import item_system
import random
import math

item_db = item_system()
user_db = database()

class ItemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="exp",description="查詢你目前的經驗值")
    async def exp(self, ctx):
        user_data = item_db.user_query(ctx.author.id)
        await ctx.respond(f"你目前擁有 {user_data["exp"]} 點經驗值！你一次釣魚可以釣起 {int(math.log10(user_data["exp"]))} 次")
    @commands.slash_command(name="item_pay",description="花費 20 個鬆餅使用一張還債卡，他可以讓你的負債歸 0")
    async def item_pay(self, ctx):
        user_data = user_db.User_Query(ctx.author.id)
        if( user_data["pancake"] < 20 ): await ctx.respond("你的鬆餅數量不足")
        else:
            if( user_data["money"] > 0 ): await ctx.respond("你明明就有錢，諧咖")
            elif( user_data["money"] == 0): await ctx.respond("你沒有負債但你也沒有錢，可撥")
            else:
                now_money = user_data["money"]
                money_change = user_db.update_user(-now_money,0)
                money_change.update_money(user_db,ctx.author.id)
                await ctx.respond("你使用了還債卡，讓你的負債歸 0 了！繼續努力，小心偷錢")

                pancake_change = user_db.update_user(0,-20)
                pancake_change.update_pancake(user_db,ctx.author.id)
    @commands.slash_command(name="item_exchange",description="花費 50 個鬆餅使用一張轉移卡，並指定 1 個人，你下次遭受到攻擊時會將攻擊對象直接轉移(無論是否成功)")
    async def item_exchange(self, ctx, member: discord.Member):
        if( user_data["pancake"] < 50 ): await ctx.respond("你的鬆餅數量不足")
        else:
            pancake_change = user_db.update_user(0,-50)
            pancake_change.update_pancake(ctx.author.id)

            new_item = [ "exchange", member ]
            item_db.item_update(item_db,ctx.author.id,new_item)


def setup(bot):
    bot.add_cog(ItemCommands(bot))