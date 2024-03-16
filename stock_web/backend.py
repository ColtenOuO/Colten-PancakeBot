from fastapi import FastAPI, Form
from pydantic import BaseModel
import sys
from pathlib import Path

app = FastAPI()

class BuyOrder(BaseModel):
    stock_amount: int
    stock_price: float

@app.post("/submit-buy-order")
async def submit_buy_order(stock_amount: int = Form(...), stock_price: float = Form(...)):
    print(f"股数: {stock_amount}, 價格: {stock_price}")
    broadcast_stock(stock_amount,stock_price)
    return {"message": f"已提交買入股票订单，股数: {stock_amount}, 價格: {stock_price}"}
