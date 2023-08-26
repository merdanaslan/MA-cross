import backtrader as bt
import pandas as pd


class SimpleCrossoverStrategy(bt.Strategy):
    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.slow_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=200)

    def next(self):
        if self.fast_ma > self.slow_ma:
            self.buy()

        elif self.fast_ma < self.slow_ma and self.position:
            self.close()


data = pd.read_csv('btc_4h_data_jan_to_aug.csv', parse_dates=True, index_col='timestamp')
data_feed = bt.feeds.PandasData(dataname=data)
cerebro = bt.Cerebro()
cerebro.adddata(data_feed)
cerebro.addstrategy(SimpleCrossoverStrategy)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
