from discord import (
    ApplicationContext,
    Bot,
    Embed,
    EmbedAuthor,
    EmbedFooter,
    Option,
    SlashCommandGroup
)

from crud.codeforces import CodeforcesData
from datetime import datetime
from math import log

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

def setup(bot: Bot):
    bot.add_cog(CodeforcesSystem(bot=bot))