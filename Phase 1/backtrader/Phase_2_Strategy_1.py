"""
I've started looking into streteggies, I'll start with VWAP-RSI combo
"""

import backtrader as bt
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf
import pandas as pd


cerebro = bt.Cerebro()

df = pd.read_csv("Detour/XBTUSD_1DayBars_BitMEX.csv")
df = pd.DataFrame(df)


class VolumeWeightedAveragePrice(bt.Indicator):

    plotinfo = dict(subplot=False)
    params = (('period', 1), )
    alias = ('VWAP', 'VolumeWeightedAveragePrice',)
    lines = ('VWAP',)
    plotlines = dict(VWAP=dict(alpha=0.50, linestyle='-.', linewidth=2.0))

    def __init__(self):
        # Before super to ensure mixins (right-hand side in subclassing)
        # can see the assignment operation and operate on the line
        cumvol = bt.ind.SumN(self.data.volume, period = self.p.period)
        typprice = ((self.data.close + self.data.high + self.data.low)/3) * self.data.volume
        cumtypprice = bt.ind.SumN(typprice, period=self.p.period)
        self.lines[0] = cumtypprice / cumvol

        super(VolumeWeightedAveragePrice, self).__init__()


class St(bt.Strategy):
    params = dict(bperiod=17, bmovav=VolumeWeightedAveragePrice,
                  bupperband=80, blowerband=19)

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(self.data, movav=VolumeWeightedAveragePrice )


data = bt.feeds.BacktraderCSVData(dataname='Detour/XBTUSD_1DayBars_BitMEX.csv')

cerebro = bt.Cerebro()
cerebro.adddata(data)
#cerebro.addstrategy(St)
cerebro.addindicator(VolumeWeightedAveragePrice)
cerebro.run()
cerebro.plot()



