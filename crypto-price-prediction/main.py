# script imports
import technical_analysis as ta
import sentiment_analysis as sa
import moving_average_macd as mama
import relative_strength_index as rsi

# get input from user
crypto = input('Enter the ticker of the cryptocurrency you want to track: ')
against = input('Enter the currency against which you want to track: ')
timeframe = int(input('Enter the number of days for which to predict: '))
hashtag = input('Enter a suggestive hashtag for the cryptocurrency you want to track: ')
days = int(input('Enter the time period of the CryptoTweeter sentiment analysis: '))

# set up analyzer objects
sentiment_analyzer = sa.Analyzer(crypto, hashtag, days)
sentiment_analyzer.plot()
sentiment = sentiment_analyzer.predict()

mama_analyzer = mama.Analyzer(timeframe)
mama_analyzer.plot()
mamacd = mama_analyzer.predict()

rsi_analyzer = rsi.Analyzer(crypto, against, timeframe)
rsi_analyzer.plot()
rsi = rsi_analyzer.predict()
print([sentiment, rsi, mamacd])
technical_analyzer = ta.Analyzer(crypto, against, timeframe)
technical_analyzer.plot()


























# pret -> 100%
#
# pret = pret + 44%2%pret
#
# sentiment 2%
# rsi 2%
# ma 2%
# macd 2%
#
# sentiment   -> daca e positiv   -> + procent% * 2%
#             -> daca e negativ   -> - procent% * 2%
#             -> daca e neutru    -> nimic
#
# rsi         -> daca e positiv   -> + procent% * 2%
#             -> daca e negativ   -> - procent% * 2%
#
# ma          -> daca e positiv   -> + procent% * 2%
#             -> daca e negativ   -> - procent% * 2%
#
# macd        -> daca e positiv   -> + procent% * 2%
#             -> daca e negativ   -> - procent% * 2%
#
# 800 pozitiv
# 600 negativ
# 400 neutru
#
# 44%