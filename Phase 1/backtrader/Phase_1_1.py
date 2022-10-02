"""
This file includes test of trategies, documentation learning and other stuff I need to check/ test before
beginning the building of the actual algorithm.
It contains repurposed/stolen/copied code from multiple sources :)
"""

#import needed libraries
import matplotlib.pyplot as plt
import backtrader as bt
import backtrader.feeds.yahoo as btfdyo
import matplotlib.pyplot as plt
from alpha_vantage.cryptocurrencies import C

# The data
cc = (key='ONXG2X4PBBZ57Y6S',output_format='pandas')

# We will retrieve daily OHLC prices, Alpha vantage also contains intraday results which are difficult to come by elsewhere
data_df, metadata_df = cc.get_currency_exchange_daily(from_symbol='USD', to_symbol='GBP', outputsize='full')

data_df.sort_index(inplace=True)
data_df = data_df.loc['2018-09-11':'2018-09-18']
print(data_df)
# Rename & rearrange the fields so they can be ingested by Backtrader
data_df = data_df.loc[:, ['2. high', '3. low', '1. open', '4. close']]
data_df.columns = ['High', 'Low', 'Open', 'Close']
print(data_df)

up = data_df[data_df.Close >= data_df.Open]
down = data_df[data_df.Close < data_df.Open]
col1 = 'blue'
col2 = 'green'
width = .3
width2 = .03
plt.bar(up.index, up.Close-up.Open, width, bottom=up.Open, color=col1)
plt.bar(up.index, up.High-up.Close, width2, bottom=up.Close, color=col1)
plt.bar(up.index, up.Low-up.Open, width2, bottom=up.Open, color=col1)
plt.bar(down.index, down.Close-down.Open, width, bottom=down.Open, color=col2)
plt.bar(down.index, down.High-down.Open, width2, bottom=down.Open, color=col2)
plt.bar(down.index, down.Low-down.Close, width2, bottom=down.Close, color=col2)
#plt.show()

class boll_bander(bt.Strategy):

    params = dict(bperiod=100)

    def __init__(self):
    # Define Bollinger band

        self.boll = bt.ind.DoubleExponentialMovingAverage(period=self.p.bperiod, plot=True, plotname='DEMA',
                                      subplot=False)

    # Define cross-over points

        self.buysig = bt.indicators.CrossOver(self.data0, self.boll.lines.dema, plotname='buy signal', plot=True)
       # self.sellsig = bt.indicators.CrossOver(self.data0, self.boll.lines.dema, plotname='sell signal', plot=True)


    def next(self):
        if not self.position:  # not in the market
            if self.buysig > 0:  # if fast crosses slow to the upside
                self.order_target_size(target=00)  # enter long

        elif self.buysig > 0:  # in the market & cross to the downside
            self.order_target_size(target=1000)

cerebro = bt.Cerebro()
data = bt.feeds.PandasData(dataname=data_df)
cerebro.adddata(data)
cerebro.addobserver(bt.observers.Value)
cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.addanalyzer(bt.analyzers.DrawDown)
cerebro.addstrategy(boll_bander)
results = cerebro.run()


sharpe = results[0].analyzers.sharperatio.get_analysis()['sharperatio']

print(f"Sharpe: {results[0].analyzers.sharperatio.get_analysis()['sharperatio']:.3f}")
print(f"Norm. Annual Return: {results[0].analyzers.returns.get_analysis()['rnorm100']:.2f}%")
print(f"Max Drawdown: {results[0].analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")
cerebro.plot(iplot=False, volume=False, width=20)"""