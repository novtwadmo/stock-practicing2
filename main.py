import twstock
import requests
import time

def fetch_and_send_stock_data():
    stock_codes = ["2330", "2317", "2412", "3008", "1301"]  # 預設要抓取的股票代碼
    stock_data = []

    for code in stock_codes:
        stock = twstock.realtime.get(code)
        if stock['success']:
            stock_info = {
                "name": stock["info"]["name"],
                "price": stock["realtime"]["latest_trade_price"],
                "high": stock["realtime"]["high"],
                "low": stock["realtime"]["low"],
                "volume": stock["realtime"]["accumulate_trade_volume"],
            }
            stock_data.append(stock_info)
    
    # 發送數據到 Render 上的 API
    api_url = "https://your-render-app.onrender.com/update_stock_data"
    try:
        response = requests.post(api_url, json={"stocks": stock_data})
        if response.status_code == 200:
            print("成功發送股票數據")
        else:
            print(f"錯誤: {response.status_code}")
    except Exception as e:
        print(f"無法連接到 API: {e}")

# 模擬每隔 10 秒抓取數據
while True:
    fetch_and_send_stock_data()
    time.sleep(10)
