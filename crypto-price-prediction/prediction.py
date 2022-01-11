# script imports
import technical_analysis as ta
import sentiment_analysis as sa
import moving_average_macd as mama
import relative_strength_index as rsi


class PredictionPlot:
    def __init__(self, crypto, fiat, time, name, twitter):
        # get input from user
        self.crypto = crypto
        self.against = fiat
        self.timeframe = time
        self.hashtag = name
        self.days = twitter

        # set up analyzer objects
        sentiment_analyzer = sa.Analyzer(self.crypto, self.hashtag, self.days)
        sentiment_analyzer.plot()
        sentiment = sentiment_analyzer.predict()

        mama_analyzer = mama.Analyzer(self.timeframe)
        mama_analyzer.plot()
        mamacd = mama_analyzer.predict()

        rsi_analyzer = rsi.Analyzer(self.crypto, self.against, self.timeframe)
        rsi_analyzer.plot()
        rsi_r = rsi_analyzer.predict()
        print([sentiment, rsi_r, mamacd])
        technical_analyzer = ta.Analyzer(self.crypto, self.against, self.timeframe)
        technical_analyzer.plot(sentiment, rsi_r, mamacd)
