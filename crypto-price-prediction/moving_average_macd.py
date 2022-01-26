import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt

import datetime as dt


class Analyzer:
    def __init__(self, ticker, against, timeframe):
        self.ticker = ticker
        self.against = against
        self.timeframe = timeframe

        self.df = web.DataReader(f'{self.ticker}-{self.against}', 'yahoo', dt.datetime(2017, 1, 1), dt.datetime.now())

        shortEMA = self.df['Adj Close'].ewm(span=12, adjust=False).mean()
        longEMA = self.df['Adj Close'].ewm(span=26, adjust=False).mean()
        period = int(self.timeframe / 5)

        self.df['SMA'] = SMA(self.df, period)

        self.MACD = shortEMA - longEMA
        self.signal = self.MACD.ewm(span=9, adjust=False).mean()
        self.df['MACD'] = self.MACD
        self.df['Signal Line'] = self.signal

        self.df['PredictionMovingAverage'] = strategyMovingAverage(self.df)
        self.df['PredictionMACD'] = strategyMACD(self.df)

    def plot(self):
        plt.figure(figsize=(12.2, 4.5))
        plt.plot(self.df.index, self.MACD, label="MACD", color='red')
        plt.plot(self.df.index, self.signal, label='Signal Line', color='blue')
        plt.legend(loc='upper left')
        plt.show()

    def predict(self):
        sum = 0

        ma_neutral = self.df['PredictionMovingAverage'].value_counts()['NT']
        ma_positive = self.df['PredictionMovingAverage'].value_counts()['PZ']
        ma_negative = self.df['PredictionMovingAverage'].value_counts()['NG']

        ma_maximum = max(ma_negative, ma_neutral, ma_positive)
        ma_percent = ma_maximum / (ma_positive + ma_neutral + ma_negative)

        if ma_maximum == ma_positive:
            sum = ma_percent
        elif ma_maximum == ma_negative:
            sum = -ma_percent

        macd_neutral = self.df['PredictionMACD'].value_counts()['NT']
        macd_positive = self.df['PredictionMACD'].value_counts()['PZ']
        macd_negative = self.df['PredictionMACD'].value_counts()['NG']

        macd_maximum = max(macd_negative, macd_neutral, macd_positive)
        macd_percent = macd_maximum / (macd_positive + macd_neutral + macd_negative)

        if macd_maximum == macd_positive:
            sum += macd_percent
        elif macd_maximum == macd_negative:
            sum += -macd_percent

        return sum


def SMA(data, period, column='Adj Close'):
    return data[column].rolling(window=period).mean()


def strategyMovingAverage(df):
    tags = []
    flag = 0
    buy_price = 0

    for i in range(0, len(df)):
        if df['SMA'][i] > df['Adj Close'][i] and flag == 0:
            tags.append('PZ')
            buy_price = df['Adj Close'][i]
            flag = 1
        elif df['SMA'][i] < df['Adj Close'][i] and flag == 1 and buy_price < df['Adj Close'][i]:
            tags.append('NG')
            buy_price = 0
            flag = 0
        else:
            tags.append('NT')
    return tags


def strategyMACD(signal):
    tags = []
    flag = -1
    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            if flag != 1:
                tags.append('PZ')
                flag = 1
            else:
                tags.append('NT')
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            if flag != 0:
                tags.append('NG')
                flag = 0
            else:
                tags.append('NT')
        else:
            tags.append('NT')
    return tags
