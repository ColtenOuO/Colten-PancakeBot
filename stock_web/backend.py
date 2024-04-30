from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx 
import os
from pydantic import BaseModel
from uvicorn import Config, Server
from discord import Bot
from bot import broadcast_buy, broadcast_sell, broadcast_match
from pymongo import MongoClient
from bot import bot
from config import API_HOST, API_PORT, MAIN_CHANNEL, STCOK_CHANNEL
from config import LOGIN_CLIENT_ID, LOGIN_CLIENT_SECRET, LOGIN_REDIRCET_URL
import json

from motor.motor_asyncio import AsyncIOMotorClient
from crud.stock import CRUDStock

crud_stock: CRUDStock = CRUDStock()
app = FastAPI()
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_URL = "https://discord.com/api/users/@me"
# 設定CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # 允許的源列表，可以使用["*"]來允許所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允許的方法列表，["*"] 表示所有
    allow_headers=["*"],  # 允許的標頭列表，["*"] 表示所有
)

@app.get("/price/{stock_id}")
async def get_price(stock_id: str):
    stock = await crud_stock.get_by_code(stock_id)
    if stock:
        return {"price": stock.price}
    return {"error": "Stock not found"}

@app.post("/submit-buy-order")
async def submit_buy_order(
    stock_code: str = Form(),
    stock_name: str = Form(),
    stock_amount: int = Form(),
    stock_price: float = Form(),
    discord_id: int = Form()
):

    print(f"股票名稱：{stock_name} 股票代碼: {stock_code}, 股数: {stock_amount}, 價格: {stock_price}")
    await broadcast_buy(discord_id=discord_id, stock_name=stock_name,stock_code=stock_code,stock_amount=stock_amount,stock_price=stock_price)
    return {"OK"}
@app.post("/submit-sell-order")
async def submit_sell_order (
    stock_code: str = Form(),
    stock_name: str = Form(),
    stock_amount: int = Form(),
    stock_price: float = Form(),
    discord_id: int = Form()
):
    print(f"股票名稱：{stock_name} 股票代碼: {stock_code}, 股数: {stock_amount}, 價格: {stock_price}")
    await broadcast_sell(discord_id=discord_id, stock_name=stock_name,stock_code=stock_code,stock_amount=stock_amount,stock_price=stock_price)
    return {"OK"} 

@app.post("/auth/callback")
async def auth_callback(request: Request):
    form_data = await request.form()
    access_code = form_data.get("code")
    token_data = {
        "client_id": LOGIN_CLIENT_ID,
        "client_secret": LOGIN_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": access_code,
        "redirect_uri": LOGIN_REDIRCET_URL
    }
    async with httpx.AsyncClient() as client:
        token_response = await client.post(DISCORD_TOKEN_URL, data=token_data)
        if token_response.status_code != 200:
            print(f"Error getting token: {token_response.text}")

        token_response_json = token_response.json()
        access_token = token_response_json.get("access_token")
        
        # 使用 access token 獲取用戶資訊
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        user_response = await client.get(DISCORD_API_URL, headers=headers)
        user_data = user_response.json()
        print(user_data)
        return user_data

@app.get("/order-match/{option}/{discord_id}/{stock_id}/{stock_name}/{price}/{amount}")
async def order_match(option: str, discord_id: int, stock_id: int, stock_name: str, price: int, amount: int):
    with open('token.json') as f:
        tokens = json.load(f)
    client = MongoClient(tokens['db_client'])
    all_stock_order = client['colten-pancake']['stock-order'].find()
    for order in all_stock_order:
        if( order['option'] != option and order['price'] == price ):
            if( discord_id == order['discord_id'] ): continue
            if( order['amount'] == amount ):
                client['colten-pancake']['stock-order'].delete_one({"option": order["option"], "discord_id": order["discord_id"], "stock_id": order["stock_id"], "price": order["price"], "amount": order["amount"]})
                
                if( option == 'buy' ): await broadcast_match(discord_id,order['discord_id'],stock_name,stock_id,amount,price)
                else: await broadcast_match(discord_id,order['discord_id'],stock_name,stock_id,amount,price)
                
                return {"status": "match"}
    client['colten-pancake']['stock-order'].insert_one({"option": option, "discord_id": discord_id, "stock_id": stock_id, "price": price, "amount": amount})
    return {"status", "no match"}
    



async def start_api():
    config = Config(
        app=app,
        host=API_HOST,
        port=API_PORT,
    )
    server = Server(config=config)

    await server.serve()

