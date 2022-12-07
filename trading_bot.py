import backtrader as bt
import datetime
from strategies import TestStrategy


cerebro = bt.Cerebro()
data = bt.feeds.YahooFinanceCSVData(
    dataname='oracle.csv',

    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2000, 12, 31),

    reverse = False
)
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)

cerebro.broker.set_cash(1000000)
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

print('Starting portfolio value: %.2f' %cerebro.broker.getvalue())



cerebro.run()
print('Ending portfolio value: %.2f' %cerebro.broker.getvalue())

import matplotlib.pyplot as plt

cerebro.plot()
