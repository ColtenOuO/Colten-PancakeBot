import discord
from discord.ext import commands
from item.item_db import item_system
from db import database
import random
import math


class Fishing:
    def __init__(self,fish_list: list = []) -> None:
        self.fish_list = fish_list
        f = open('fish.txt','r',encoding="utf-8")
        for i in f.readlines():
            i.replace("\n",",")
            self.fish_list.append(i)
    def get_fish(self) -> str:
        return random.choice(self.fish_list)

fishing_instance = Fishing()  # Renamed variable to avoid naming conflict
db = database()
item_db = item_system()

for i in db.client.pythondb["discord_user_data"].find():
    if( item_db.user_query(i["discord_id"]) == None ): item_db.user_adding(i["discord_id"])

class FishingCommands(commands.Cog):
    def __init__(self, bot):
        self.random_fish = Fishing()
        self.bot = bot
    
    @commands.slash_command(name="fishing",description="釣起一隻魚，目前釣起高睿的機率為 1/90 !")
    async def fishing_cmd(self, ctx):  # Renamed function to avoid naming conflict
        
        DATA = item_db.user_query(ctx.author.id)
        fish_list = []
        total: int = 0
        total_times: int = int(math.log10(DATA["exp"]))
        print(total_times)
        while(total_times != 0):
            print(i)
            fish_result = fishing_instance.get_fish()
            fish_result = fish_result.replace("\n","")
            fish_list.append(fish_result)
            cm = round(random.uniform(0, 1000))
            dv = round(random.uniform(1, 20))
            total += int( cm / dv )
            total_times -= 1

        
        if( db.Register_Query(ctx.author.id) == False ): db.Registered(ctx.author.id)
        symbol = ","
        await ctx.respond(f"你共釣起了 {len(fish_list)} 隻魚，他們分別是 {symbol.join(fish_list)}，你總共獲得了 {total} 元")
        
        adding_money = db.update_user(total,0)
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
        if( target_money == 1 ): target_money += 1
        steal_money = round(random.uniform(0,target_money/2))
        if( ctx.author.id == member.id ): await ctx.respond("你偷你自己幹嘛？？你結帳 +10")
        elif( target_money <= 0 ): await ctx.respond("你想偷的人已經負債或沒有錢了！不要再偷他了QQ")
        elif( db.User_Query(ctx.author.id)["money"] < 0 ): await ctx.respond("你現在都負債了還想偷錢R")
        elif( num >= 70 ):
            await ctx.respond(f"Successful Stealing！你偷走了 {member} {steal_money} 元")
            money_change = db.update_user(-steal_money,0)
            money_change.update_money(db,member.id)

            adding_money = db.update_user(steal_money,0)
            adding_money.update_money(db,ctx.author.id)

            expect_exp = round(random.uniform(0,50))
            await ctx.send(f"由於 {ctx.author.mention} 成功偷取別人的財產，獲得了 {expect_exp} 點經驗值")
            item_db.exp_update(item_db,ctx.author.id,expect_exp)
            
        else:
            num = round(random.uniform(0,target_money/5))
            money_change = db.update_user(-num,0)
            money_change.update_money(db,ctx.author.id)

            pancake_get = round(random.uniform(0,10))
            adding_pancake = db.update_user(0,pancake_get)
            adding_pancake.update_pancake(db,member.id)

            await ctx.respond(f"Unsuccessful Stealing，你嘗試偷取 {member} 的錢失敗，損失了 {num} 元")
            await ctx.send(f"【公告】由於 {member} 遭到偷取財產失敗，因此獲得 {pancake_get} 個鬆餅")
    
    @commands.slash_command(name="pancake",description="查詢你現在有幾個鬆餅")
    async def Pancake(self, ctx):
        ans = db.User_Query(ctx.author.id)
        if( ans == None ): await ctx.respond("你現在擁有 0 個鬆餅")
        else:
            await ctx.respond(f"你現在擁有 {ans["pancake"]} 個鬆餅")
            if( ans["pancake"] < 0 ): await ctx.send("為什麼你的鬆餅數量是負數？？？你是不是一直在想辦法從系統偷到更多鬆餅")
    @commands.slash_command(name="pancake_exchange",description="把鬆餅拿去換錢")
    async def Pancake_Exchange(self, ctx, cnt: int):
        DATA = db.User_Query(ctx.author.id)
        if( cnt > DATA["pancake"] ): await ctx.respond("你根本沒有這麼多的鬆餅，不要以為我不知道！")
        elif( cnt == 0 ): await ctx.respond("你沒有要換任何鬆餅那你找我幹嘛？，你結帳+10")
        elif( cnt < 0 ):
            await ctx.respond(f"你為什麼要輸入負數？你完蛋了，我要把你輸入的東西變成你鬆餅增加的數量，所以你的鬆餅數量增加了 {cnt} 個")
            pancake_cahange = db.update_user(0,cnt)
            pancake_cahange.update_pancake(db,ctx.author.id)
        else:
            pancake_cahange = db.update_user(0,-cnt)
            pancake_cahange.update_pancake(db,ctx.author.id)

            adding_money = db.update_user(cnt*100,0)
            adding_money.update_money(db,ctx.author.id)

            await ctx.respond(f"兌換成功！你兌換了 {cnt} 個鬆餅")



def setup(bot):
    bot.add_cog(FishingCommands(bot))