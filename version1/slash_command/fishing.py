import discord
from discord.ext import commands
from db import database
import random


class Fishing:
    def __init__(self,fish_list: list = []) -> None:
        self.fish_list = fish_list
        f = open('fish.txt','r',encoding="utf-8")
        for i in f.readlines():
            self.fish_list.append(i)
    def get_fish(self) -> str:
        return random.choice(self.fish_list)

fishing_instance = Fishing()  # Renamed variable to avoid naming conflict
db = database()

class FishingCommands(commands.Cog):
    def __init__(self, bot):
        self.random_fish = Fishing()
        self.bot = bot
    
    @commands.slash_command(name="fishing",description="釣起一隻魚，目前釣起高睿的機率為 1/90 !")
    async def fishing_cmd(self, ctx):  # Renamed function to avoid naming conflict
        fish_result = fishing_instance.get_fish()
        cm = round(random.uniform(0, 1000))
        dv = round(random.uniform(1, 200))
        
        if( db.Register_Query(ctx.author.id) == False ): db.Registered(ctx.author.id)
        get_money: int
        get_money = int(cm / dv)
        
        await ctx.respond(f"你釣起了一隻 {cm} cm 的 {fish_result} 獲得了 {get_money} 元")
        
        adding_money = db.update_user(get_money,0)
        adding_money.update_money(db,ctx.author.id)
    
    @commands.slash_command(name="money",description="查詢自己有多少錢")
    async def money(self, ctx):  # Renamed function to avoid naming conflict 
        ans = db.Register_Query(ctx.author.id)
        if( ans == False ): await ctx.respond("你目前有 0 元，哈哈")
        else: await ctx.respond(f"你目前有 {db.User_Query(ctx.author.id)["money"]} 元！")

    @commands.slash_command(name="steal",description="嘗試偷走某個人的錢")
    async def steal(self, ctx, member: discord.Member):
        num = round(random.uniform(0,100))
        print(num)
        target_money = db.User_Query(member.id)["money"]
        steal_money = round(random.uniform(0,target_money/2))
        if( num >= 70 ):
            await ctx.respond(f"Successful Stealing！你偷走了 {member.mention} {steal_money} 元")
            money_change = db.update_user(-steal_money,0)
            money_change.update_money(db,member.id)

            adding_money = db.update_user(steal_money,0)
            adding_money.update_money(db,ctx.author.id)

        else:
            num = round(random.uniform(0,target_money/5))
            money_change = db.update_user(-num,0)
            money_change.update_money(db,ctx.author.id)

            pancake_get = round(random.uniform(0,3))
            adding_pancake = db.update_user(0,pancake_get)
            adding_pancake.update_pancake(db,member.id)

            await ctx.respond(f"Unsuccessful Stealing，你嘗試偷取 {member.mention} 的錢失敗，損失了 {num} 元")
            await ctx.send(f"【公告】由於 {member.mention} 遭到偷取財產失敗，因此獲得 {pancake_get} 個鬆餅")



def setup(bot):
    bot.add_cog(FishingCommands(bot))