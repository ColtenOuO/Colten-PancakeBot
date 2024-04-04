from discord import (
    ApplicationContext,
    Bot,
    Embed,
    EmbedAuthor,
    EmbedFooter,
    Option,
    SlashCommandGroup
)
from config import MAIN_CHANNEL, TOKEN
from crud.codeforces import CodeforcesData
from datetime import datetime
from math import log
from asyncio import get_event_loop, sleep as asleep
from schemas import UserUpdate

from .base import GroupCog, UserCog
from pymongo import MongoClient
import json
import requests

with open('config.json') as f:
    tokens = json.load(f)
    client = MongoClient(tokens['mongodb']['srvServiceName'])
class CodeforcesSystem(GroupCog):
    bot: Bot
    codeforcesdata: CodeforcesData = CodeforcesData()
    group = SlashCommandGroup(
        name="codeforces",
        description="codeforces"
    )

    @group.command(
        name="query",
        description="查詢 codeforces handle 的資料"
    )
    async def query_handle(self, ctx: ApplicationContext,handle: str):
        embed = self.codeforcesdata.get_info_by_handle(handle=handle)
        if( embed == None ): await ctx.respond('查無此人，搞什麼')
        else: await ctx.respond(embed=embed)
    
    @group.command(
        name="problem",
        description="隨便戳一題 Codeforces 的題目"
    )
    async def random_problem(self, ctx: ApplicationContext):
        data = self.codeforcesdata.get_problem_by_rating()
        if( data == None ): await ctx.respond('System Error! 高睿結帳+10')
        else: await ctx.respond(f'https://codeforces.com/contest/{data["contestId"]}/problem/{data["index"]}')
    @group.command(
        name="practice",
        description="隨便戳一題 Codeforces 的題目"
    )
    async def practice_problem(self, ctx: ApplicationContext):
        problem_data = self.codeforcesdata.get_problem_by_rating()
        if( problem_data == None ): await ctx.respond('System Error! 高睿結帳+10')
        else:
            await ctx.respond(f'https://codeforces.com/contest/{problem_data["contestId"]}/problem/{problem_data["index"]}')
            await ctx.send(f'{ctx.author.mention}, 你有 10 分鐘的時間解決掉這一題，請加油！')
            times: int = 600
            while( times != 0 ):
                status = self.codeforcesdata.get_status_by_handle()
                if( status['problem']['contestId'] == problem_data['contestId'] and status['problem']['index'] == problem_data['index'] ):
                    verdict = status['verdict']
                    print(status)
                    if( verdict == 'OK' ): await ctx.send(f"'f{ctx.author.mention}' 成功 Accepted 了這題！")
                    else: await ctx.send(f"f'{ctx.author.mention}' 嘗試上傳了這題，不料得到了一個 f{verdict}，哈哈") 
                await asleep(1)
                times -= 1
                if( times == 0 ):
                    await ctx.send(f'時間到！{ctx.author.mention} 無法在時間內解出題目，結帳+10')

def setup(bot: Bot):
    bot.add_cog(CodeforcesSystem(bot=bot))