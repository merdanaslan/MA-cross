import backtrader as bt
import pandas as pd


class EMACrossoverStrategy(bt.Strategy):
    params = (
        ("fast_period", 50),
        ("slow_period", 200),
    )

    def __init__(self):
        self.ema_fast = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.fast_period)
        self.ema_slow = bt.indicators.ExponentialMovingAverage(self.data.close, period=self.p.slow_period)

    def next(self):
        if self.ema_fast[0] > self.ema_slow[0] and self.ema_fast[-1] <= self.ema_slow[-1]:
            self.buy()

        elif self.ema_fast[0] < self.ema_slow[0] and self.ema_fast[-1] >= self.ema_slow[-1]:
            self.sell()


# Load data from CSV
data = pd.read_csv('btc_4h_data_jan_to_aug.csv', parse_dates=True, index_col='timestamp')

data_feed = bt.feeds.PandasData(dataname=data)

cerebro = bt.Cerebro()

cerebro.adddata(data_feed)

cerebro.addstrategy(EMACrossoverStrategy)

# Set starting cash amount
cerebro.broker.set_cash(10000)

# Set commission
cerebro.broker.setcommission(commission=0.001)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()
