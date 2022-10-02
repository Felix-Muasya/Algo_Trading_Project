from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
import pandas as pd  # for reading data
import backtrader as bt
import backtrader.indicators as btind


class vwap(bt.Indicator):
    ''' This indicator needs a timer to reset the period to 1 at every session start
        also it needs a flag in next section of strategy to increment the self._vwap_period
        run cerebro with runonce=False as we need dynamic indicator'''

    plotinfo = dict(subplot=False)

    alias = ('VWAP', 'VolumeWeightedAveragePrice', 'vwap',)
    lines = ('VWAP', 'typprice', 'cumprice', 'cumtypprice',)
    plotlines = dict(VWAP=dict(alpha=1.0, linestyle='-', linewidth=2.0, color='magenta'))

    def __init__(self):
        self._vwap_period = 1

    def vwap_period(self, period):
        self._vwap_period = period

    def next(self):
        self.l.typprice[0] = ((self.data.close + self.data.high + self.data.low) / 3) * self.data.volume
        self.l.cumtypprice[0] = sum(self.l.typprice.get(size=self._vwap_period), self._vwap_period)
        self.cumvol = sum(self.data.volume.get(size=self._vwap_period), self._vwap_period)
        self.lines.VWAP[0] = self.l.cumtypprice[0] / self.cumvol

        # super(vwap, self).__init__()


# Create a Stratey
class strat(bt.Strategy):
    params = dict(
        vwap_period=1,
        when=bt.timer.SESSION_START,
    )

    def __init__(self):
        self.vwap = vwap(self.data)  # get VWAP

        self.add_timer(
            when=self.p.when,
        )

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

    def notify_timer(self, timer, when, *args, **kwargs):
        self.vwap_period = 1

    def next(self):
        ## Use the method insread of changing param
        self.vwap.vwap_period(self.vwap_period)

        ##  print values for diagnostics
        txt = list()
        txt.append('{}'.format(len(self.data0)))
        txt.append('{}'.format(self.data.datetime.datetime(0)))
        txt.append('{}'.format(self.data.close[0]))
        txt.append('{}'.format(self.vwap[0]))
        txt.append('{}'.format(self.vwap_period))
        # print(', '.join(txt))

        # Increment the Period
        self.vwap_period += 1


## Setup cerebro
cerebro = bt.Cerebro()

## Add a strat
#cerebro.addstrategy(strat)

cerebro.addindicator(vwap)

## input data file
data_file = 'Detour/XBTUSD_1DayBars_BitMEX.csv'

# Create a Data Feed and add to cerebro
df = pd.read_csv(data_file, header=0, index_col=0, parse_dates=True)
data0 = bt.feeds.PandasData(dataname=df, \
                            name="nifty"
                            )

# add data
cerebro.adddata(data0)

## Run it with runonce=False
cerebro.run(runonce=False)

# Plot the data
cerebro.plot()

data_file = '../Detour/XBTUSD_MinuteBars_BitMEX.csv'

# Create a Data Feed and add to cerebro
df = pd.read_csv(data_file, header=0, index_col=0, parse_dates=True)
data = bt.feeds.PandasData(dataname=df, \
                           name="BTC_Trades"
                           )