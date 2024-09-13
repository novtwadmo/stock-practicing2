# -*- coding: utf-8 -*-

"""import datetime
import concurrent.futures
from flask import Flask, render_template, jsonify
import twstock

app = Flask(__name__)

stock_list = [
    '2330',  # 台積電
    '2317',  # 鴻海
    '1301',  # 台塑
    '1326',  # 台化
    '2412',  # 中華電
    '3008',  # 大立光
    '1303',  # 南亞
    '2308',  # 台達電
    '2454',  # 聯發科
    '2881',  # 富邦金
    '8299',  # 群聯
    '6223',
]

stock_name = {
    '2330': u'台積電',
    '2317': u'鴻海',
    '1301': u'台塑',
    '1326': u'台化',
    '2412': u'中華電',
    '3008': u'大立光',
    '1303': u'南亞',
    '2308': u'台達電',
    '2454': u'聯發科',
    '2881': u'富邦金',
    '8299': u'群聯',
    '6223': '旺矽'
}


@app.route('/')
def stocker():
    st = {}
    for sid in stock_list:
        s = Stock(sid)
        b = BestFourPoint(s)
        bfp = b.best_four_point()
        buy_or_sell = "hmmmm, don't touch"
        if bfp and bfp[0] is True:
            buy_or_sell = "Buy it: " + bfp[1]
        elif bfp and bfp[0] is False:
            buy_or_sell = "Sell it: " + bfp[1]

        st[str(s.sid)] = {'pivot': buy_or_sell, 'price': s.price[-5:]}

    return render_template('stocker.html',
                           stock_id=stock_list,
                           stock=st,
                           name=stock_name)


@app.route('/stocks/prices/<string:stock_id>')
def get_stock_price(stock_id):
    s = Stock(stock_id)
    ret = []
    today = datetime.datetime.today()
    stock_closing = 1 if today < today.replace(hour=13, minute=30, second=0) else 0
    for index, i in enumerate(s.price[-5:]):
        date = today - datetime.timedelta(days=(4 - index + stock_closing))
        ret.append(
            {
                'date': date.strftime('%Y-%m-%d'),
                'price': i,
            }
        )
    return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True)"""

"""from flask import Flask, render_template, request
import twstock

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    if request.method == 'POST':
        stock_id = request.form.get('stock_id')
        stock_data = twstock.realtime.get(stock_id)
    return render_template('index.html', stock_data=stock_data)

if __name__ == '__main__':
    app.run(debug=True)"""

from flask import Flask, render_template
import twstock

app = Flask(__name__)

def get_top_10_stocks():
    all_stocks = twstock.codes
    stock_info = []
    
    for stock_id in all_stocks:
        stock = twstock.Stock(stock_id)
        stock.fetch_from(2024, 9)  # 取得當前月的資料
        if stock.price and stock.capacity:
            stock_info.append({
                'name': stock.sid,
                'price': stock.price[-1],
                'volume': stock.capacity[-1],
                'price_change': stock.change
            })

    # 根據成交量排序並取得前十支
    sorted_stocks = sorted(stock_info, key=lambda x: x['volume'], reverse=True)[:10]
    return sorted_stocks

@app.route('/')
def index():
    top_10_stocks = get_top_10_stocks()
    return render_template('index.html', stocks=top_10_stocks)

if __name__ == '__main__':
    app.run(debug=True)

