from fastapi import FastAPI, Form
from pydantic import BaseModel
from uvicorn import Config, Server
from discord import Bot
from bot import broadcast_buy

from bot import bot
from config import API_HOST, API_PORT, MAIN_CHANNEL

app = FastAPI()

class BuyOrder(BaseModel):
    stock_code: str  # 添加股票代碼字段
    stock_amount: int
    stock_price: float

@app.post("/submit-buy-order")
async def submit_buy_order(
    stock_code: str = Form(),  # 接收股票代碼
    stock_amount: int = Form(),
    stock_price: float = Form()
):
    # 處理買入訂單，使用stock_code來識別股票
    print(f"股票代碼: {stock_code}, 股数: {stock_amount}, 價格: {stock_price}")
    await broadcast_buy(stock_id=stock_code,stock_amount=stock_amount,stock_price=stock_price)
    # 示例回應
    return {"message": f"已提交買入股票訂單，股票代碼: {stock_code}, 股数: {stock_amount}, 價格: {stock_price}"}


async def start_api():
    config = Config(
        app=app,
        host=API_HOST,
        port=API_PORT,
    )
    server = Server(config=config)

    await server.serve()
