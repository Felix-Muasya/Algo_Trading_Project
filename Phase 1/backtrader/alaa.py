import backtrader as bt
from datetime import datetime

cerebro = bt.Cerebroi
data = bt.feeds.YahooFinanceData(dataname = 'AAPL', fromdate = datetime(2010, 1, 1), todate = datetime(2020, 1, 1))
cerebro.adddata(data)