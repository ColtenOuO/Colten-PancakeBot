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

with open('token.json') as f:
    tokens = json.load(f)
    client = MongoClient(tokens['mongodb'].srvServiceName)
class CodeforcesSystem:
    bot: Bot
    group = SlashCommandGroup(
        name="mining",
        description="Mining"
    )

    def __init__(self, bot) -> None:
        self.bot = bot
        self.codeforcesdata: CodeforcesData = CodeforcesData()

    @group.command(
        name="query",
        description="查詢 codeforces handle 的資料"
    )
    async def start_mining(self, ctx: ApplicationContext,handle: str):
        ctx.respond(self.codeforcesdata(handle))

