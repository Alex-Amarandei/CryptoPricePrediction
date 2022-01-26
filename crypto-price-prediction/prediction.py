import pandas_datareader as web

import neural_network as nn
import sentiment_analysis as sa
import moving_average_macd as mama
import relative_strength_index as rsi

from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PricePredictor:
    def __init__(self, root, ticker, against, name, timeframe, twitter_timeframe):
        self.root = root
        self.ticker = ticker
        self.against = against
        self.name = name
        self.timeframe = timeframe
        self.twitter_timeframe = twitter_timeframe

        sentiment_analyzer = sa.Analyzer(self.ticker, self.name, self.twitter_timeframe)
        sentiment_analyzer.plot()
        sentiment = sentiment_analyzer.predict()

        mama_analyzer = mama.Analyzer(self.ticker, self.against, self.timeframe)
        mama_analyzer.plot()
        mamacd = mama_analyzer.predict()

        rsi_analyzer = rsi.Analyzer(self.ticker, self.against, self.timeframe)
        rsi_analyzer.plot()
        rsi_r = rsi_analyzer.predict()

        neural_network_analyzer = nn.Analyzer(self.ticker, self.against, self.timeframe)
        neural_network_analyzer.plot(self.root, sentiment, rsi_r, mamacd)
