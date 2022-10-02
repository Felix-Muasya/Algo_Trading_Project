import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib
from datetime import datetime
import yfinance as yf

cerebro = bt.Cerebro()

df = yf.download('GBPUSD=X', start='2010-01-01')


feed = bt.feeds.PandasData(dataname=df)


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=50,  # period for the fast moving average
        pslow=100   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

cerebro.addstrategy(SmaCross)
cerebro.adddata(feed)
cerebro.broker.setcommission(commission=0.005)
cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name="areturn")
teststrat = cerebro.run()
print(teststrat[0].analyzers.areturn.get_analysis())
cerebro.plot()


