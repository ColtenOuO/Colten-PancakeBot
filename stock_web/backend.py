from fastapi import FastAPI, Form
from pydantic import BaseModel
from uvicorn import Config, Server

from bot import bot
from config import API_HOST, API_PORT, MAIN_CHANNEL

app = FastAPI()


class BuyOrder(BaseModel):
    stock_amount: int
    stock_price: float


@app.post("/submit-buy-order")
async def submit_buy_order(
    stock_amount: int = Form(),
    stock_price: float = Form()
):
    print(f"股数: {stock_amount}, 價格: {stock_price}")

    await bot.get_channel(MAIN_CHANNEL).send(f"Colten 委託買入 {stock_amount} 股 玻璃質量測試股份有限公司的股票，開價每股 {stock_price}")
    return {"message": f"已提交買入股票訂單，股数: {stock_amount}, 價格: {stock_price}"}


async def start_api():
    config = Config(
        app=app,
        host=API_HOST,
        port=API_PORT,
    )
    server = Server(config=config)

    await server.serve()
