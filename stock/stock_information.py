from pymongo import MongoClient
from stock.stock import StockSystem
import json
import discord
import random

with open('token.json') as f:
    tokens = json.load(f)
    client = MongoClient(tokens['db_client'])


def information():
    stocksystem = StockSystem()
    stock1_price = stocksystem.get_price('1')
    num1 = round(random.uniform(-5000,5000))
    if( stock1_price + num1 < 0 ): num1 = -(stock1_price - 1) 
    stocksystem.update_one('1',num1)
    additional = ""
    if( num1 > 0 ): additional = '+'


    embed = discord.Embed(title="今日股市變動！！！",
                      description="投資一定有風險，基金投資有賺有賠，申購前應詳閱公開說明書")
    embed.add_field(name="高睿股份有限公司",
                    value=f"目前股市狀況 (1 股價格): {stock1_price+num1} 元 (價格變動: {additional}{num1})",
                    inline=False)
    embed.add_field(name="YEE 問題不大股份有限公司",
                    value="目前股市概況 (1 股價格): 即將上市",
                    inline=False)
    embed.add_field(name="美麗橋建設股份有限公司",
                    value="目前股市概況 (1 股價格): 即將上市",
                    inline=False)

    embed.set_image(url="https://stickershop.line-scdn.net/stickershop/v1/product/6287/LINEStorePC/main.png?v=1")

    embed.set_thumbnail(url="https://down-tw.img.susercontent.com/file/22b1fc845e5ce92481d08c79ffa29296")

    return embed