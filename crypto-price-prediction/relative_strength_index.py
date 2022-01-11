# imports
import pandas as pd
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, crypto, against, timeframe):
        self.crypto = crypto
        self.against = against
        self.timeframe = timeframe

        self.start = dt.datetime(2017, 1, 1)
        self.end = dt.datetime.now()

        data = web.DataReader(f'{self.crypto}-{self.against}', 'yahoo', self.start, self.end)

        delta = data['Adj Close'].diff(1)
        delta.dropna(inplace=True)

        positive = delta.copy()
        positive[positive < 0] = 0

        negative = delta.copy()
        negative[negative > 0] = 0

        average_gain = positive.rolling(window=self.timeframe).mean()

        average_loss = abs(negative.rolling(window=self.timeframe).mean())

        relative_strength = average_gain / average_loss
        RSI = 100.0 - (100.0 / (1.0 + relative_strength))

        self.combined = pd.DataFrame()
        self.combined['Adj Close'] = data['Adj Close']
        self.combined['RSI'] = RSI

    def plot(self):
        plt.figure(figsize=(12, 8))
        ax1 = plt.subplot(211)
        ax1.plot(self.combined.index, self.combined['Adj Close'], color='lightgray')
        ax1.set_title('Adjusted Close Price', color='white')
        ax1.grid(True, color='#555555')
        ax1.set_axisbelow(True)
        ax1.set_facecolor('black')
        ax1.figure.set_facecolor('#121212')
        ax1.tick_params(axis='x', color='white')
        ax1.tick_params(axis='y', color='white')

        ax2 = plt.subplot(212, sharex=ax1)
        ax2.plot(self.combined.index, self.combined['RSI'], color='lightgray')
        ax2.axhline(0, linestyle='--', alpha=0.5, color='#ff0000')
        ax2.axhline(10, linestyle='--', alpha=0.5, color='#ffaa00')
        ax2.axhline(20, linestyle='--', alpha=0.5, color='#00ff00')
        ax2.axhline(30, linestyle='--', alpha=0.5, color='#cccccc')

        ax2.axhline(70, linestyle='--', alpha=0.5, color='#cccccc')
        ax2.axhline(80, linestyle='--', alpha=0.5, color='#00ff00')
        ax2.axhline(90, linestyle='--', alpha=0.5, color='#ffaa00')
        ax2.axhline(100, linestyle='--', alpha=0.5, color='#ff0000')

        ax2.set_title('Adjusted Close Price', color='white')
        ax2.grid(False)
        ax2.set_axisbelow(True)
        ax2.set_facecolor('black')
        ax2.figure.set_facecolor('#121212')
        ax2.tick_params(axis='x', color='white')
        ax2.tick_params(axis='y', color='white')

        plt.show()

    def predict(self):
        overbought = len(self.combined['RSI'][lambda x: x >= 70])  # will decrease
        oversold = len(self.combined['RSI'][lambda x: x <= 30])  # will increase

        if oversold == 0:
            return -1

        if overbought == 0:
            return 1

        if overbought > oversold:
            return -1 * (overbought / (oversold + overbought))
        else:
            return oversold / (oversold + overbought)
