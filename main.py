from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 全局變數保存股票數據
stock_data = []

# 定義接收股票數據的模型
class Stock(BaseModel):
    name: str
    price: str
    yesterday: str
    high: str
    low: str
    volume: str

# 定義接收請求數據的格式
class StockRequest(BaseModel):
    stocks: list[Stock]

# 提供更新股票數據的API
@app.post("/update_stock_data")
async def update_stock_data(data: StockRequest):
    global stock_data
    stock_data = data.stocks
    return {"message": "Stock data updated successfully"}

# 提供網頁前端
@app.get("/")
async def get_stock_info(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "stocks": stock_data})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
