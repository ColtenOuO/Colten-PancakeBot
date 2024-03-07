import discord
from discord.ext import commands
from db import database
from item.item_db import item_system
import random
import math

item_db = item_system()

class ItemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="exp",description="查詢你目前的經驗值")
    async def exp(self, ctx):
        user_data = item_db.user_query(ctx.author.id)
        await ctx.respond(f"你目前擁有 {user_data["exp"]} 點經驗值！你一次釣魚可以釣起 {int(math.log10(user_data["exp"]))} 次")

def setup(bot):
    bot.add_cog(ItemCommands(bot))