import backtrader as bt
import datetime
from strategies import TestStrategy





training =[]
validation = []
test = []
for i in range(20):
    cerebro = bt.Cerebro()
    data = bt.feeds.YahooFinanceCSVData(
        dataname='oracle.csv',

        fromdate=datetime.datetime(1995+i, 1, 1),
        todate=datetime.datetime(1995+i, 12, 31),

        reverse = False
    )
    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy)

    cerebro.broker.set_cash(1000000)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

    cerebro.run()

    # Return over one year
    returns = (cerebro.broker.getvalue()/1000000-1)*100

    if i<14:
        training.append(returns)
    elif i<17:
        validation.append(returns)
    else:
        test.append(returns)

# calcul of average returns
training_returns = sum(training)/14
validation_returns = sum(validation)/3
test_returns = sum(test)/3

print('trainig :',training_returns)
print('validation :',validation_returns)
print('testing :',test_returns)

#print(f'Average returns of {training_returns:0.2f} % for the training')
# print(f'Average returns of {:0.2f} % for the validation ')
# print(f'Average returns of {test_returns:0.2f} % for the testing ')
