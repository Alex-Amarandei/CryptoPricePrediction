# script imports
import technical_analysis as ta
import sentiment_analysis as sa
import relative_strength_index as rsi

# get input from user
crypto = input('Enter the ticker of the cryptocurrency you want to track: ')
hashtag = input('Enter a suggestive hashtag for the cryptocurrency you want to track: ')
against = input('Enter the currency against which you want to track: ')
timeframe = int(input('Enter the number of days for which to track: '))
days = int(input('Enter the time period of the CryptoTweeter sentiment analysis: '))

# set up analyzer objects
rsi_analyzer = rsi.Analyzer(crypto, against, timeframe)
technical_analyzer = ta.Analyzer(crypto, against, timeframe)
sentiment_analyzer = sa.Analyzer(crypto, hashtag, days)

rsi_analyzer.plot()
technical_analyzer.plot()
sentiment_analyzer.plot()
