import backtrader as bt

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.stop_loss = 0.80

    def notify_order(self,order):
        if order.status in [order.Submitted,order.Accepted]:
            return
        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1] and self.dataclose[-1] < self.dataclose[-2] :
                # Three day down in a row

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:

            if self.data.low[0]<self.position.price*self.stop_loss:
                # SELL -> stop loss hit
                sell_price = self.position.price*self.stop_loss
                self.log('SELL CREATE, %.2f' % sell_price)
                self.order = self.sell(price = sell_price)

            if len(self)>= self.bar_executed+5:

                # SELL
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
