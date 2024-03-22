import requests
import json
from discord import (
    ApplicationContext,
    Bot,
    Embed,
    EmbedAuthor,
    EmbedFooter,
    Option,
    SlashCommandGroup
)
import discord
from datetime import datetime
class CodeforcesData:
    def get_rating_by_handle(self,handle: str) -> int:
        url = "https://codeforces.com/api/user.info"
        data = { "handles": handle }
        access_token = requests.post(url, data = data)
        if( access_token.json()['status'] != 'OK' ):
            return 'No User'
        return access_token.json()['result'][0]
    def get_info_by_handle(self,handle: str):
        url = "https://codeforces.com/api/user.info"
        data = { "handles": handle }
        access_token = requests.post(url, data = data)
        if( access_token.json()['status'] != 'OK' ):
            return None
        data = access_token.json()['result'][0]
        embed = discord.Embed(title=f"{data['handle']} - {data['firstName']} {data['lastName']}",
                      url=f"https://codeforces.com/profile/{data['handle']}",
                      colour=0x00b0f4,
                      timestamp=datetime.now())
        embed.set_author(name="競技程式設計選手資料 (Codeforces)",
                        url=f"https://codeforces.com/profile/{data['handle']}")

        embed.add_field(name="組織",
                        value=data['organization'],
                        inline=False)
        embed.add_field(name="國家",
                        value=data['country'],
                        inline=False)
        embed.add_field(name="歷年最高積分",
                        value=data['maxRating'],
                        inline=True)
        embed.add_field(name="歷年最高級別",
                        value=data['maxRank'],
                        inline=True)
        embed.add_field(name="當前積分",
                        value=data['rating'],
                        inline=False)
        embed.add_field(name="當前級別",
                        value=data['rank'],
                        inline=True)
        embed.add_field(name="選手生涯",
                        value=f"{round((data['lastOnlineTimeSeconds'] - data['registrationTimeSeconds']) / 31536000)} 年",
                        inline=False)

        embed.set_image(url="https://userpic.codeforces.org/1416227/title/ff127beae02a9464.jpg")

        embed.set_thumbnail(url=data['titlePhoto'])

        embed.set_footer(text="Codeforces 選手資料",
                        icon_url="https://userpic.codeforces.org/1416227/title/ff127beae02a9464.jpg")

        return embed