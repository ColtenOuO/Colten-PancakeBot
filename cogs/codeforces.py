from discord import (
    ApplicationContext,
    Bot,
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
        rating = self.codeforcesdata.get_rating_by_handle(handle)['rating']
        rank = self.codeforcesdata.get_rating_by_handle(handle)['rank']
        await ctx.respond(f'{handle} 的 Codeforces 分數為 {rating}，等級是 {rank} !')

def setup(bot: Bot):
    bot.add_cog(CodeforcesSystem(bot=bot))