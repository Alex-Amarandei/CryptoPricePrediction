import re
import spacy
import string
import tweepy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from textblob import TextBlob
from nltk.corpus import stopwords
from datetime import datetime, timedelta
from wordcloud import WordCloud, STOPWORDS

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


class Analyzer:
    def __init__(self, crypto, hashtag, days=6):
        self.crypto = crypto
        self.hashtag = hashtag
        self.days = days

        self.client = tweepy.Client(
            bearer_token='AAAAAAAAAAAAAAAAAAAAAEe6XwEAAAAAPogu71snTvhKNPhyHw0dBx3Tgv4%3DziWKDL2YeFv5MexM9Q0U22xENU7GaeSj3v3OPVGPhC0iRKIj8G',
            consumer_key='xnHWjwH9gDKhGGEdrtsUR63tm',
            consumer_secret='z6A02iii5xj5LWxiJqw1TVAIdKJ2NUy96g3J8DaYPpvdgIksxu',
            access_token='1480221859916484608-zYLRVdNRtf8ojX1yLRuntz4yZE029D',
            access_token_secret='nylyIvtQgnvA9zODUo3GE8DfIrdfUGCZmzDbHR3vk9lCD')

        self.interval = 6

        search_term = '#' + self.crypto + ' #' + self.hashtag + ' -is:retweet lang:en'
        all_tweets = []
        date_to_fetch = datetime.today()

        for i in range(1, 20):
            date_to_fetch = date_to_fetch - timedelta(hours=self.interval)
            current_start_date = date_to_fetch.isoformat("T") + "Z"
            tweets = self.client.search_recent_tweets(query=search_term, start_time=current_start_date, max_results=100)
            for tweet in tweets.data:
                all_tweets.append(tweet.text)

        self.df = pd.DataFrame(all_tweets, columns=['Tweets'])
        self.df.drop_duplicates(subset=None, keep='first')

        self.df['Tweets'] = self.df['Tweets'].apply(lambda x: " ".join(x.lower() for x in x.split()))
        self.df['Tweets'] = self.df['Tweets'].str.replace('[^\w\s]', '')

        self.df['Tweets'] = self.df['Tweets'].apply(lambda x: remove_emoji(x))

        stop = stopwords.words('english')
        self.df['Tweets'] = self.df['Tweets'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
        self.df['Tweets'] = self.df['Tweets'].apply(space)
        self.df['Tweets'] = self.df['Tweets'].apply(self.clean_tweet)
        self.df.head()

        self.df['Subjectivity'] = self.df['Tweets'].apply(get_subjectivity)
        self.df['Polarity'] = self.df['Tweets'].apply(get_polarity)
        self.df['Decision'] = self.df['Polarity'].apply(get_sentiment)
        self.df.head()

    def plot(self):
        plt.style.use('fivethirtyeight')
        plt.figure(figsize=(8, 6))
        for i in range(0, self.df.shape[0]):
            plt.scatter(self.df['Polarity'][i], self.df['Subjectivity'][i], color='Purple')
        plt.title('Altcoin decision Scatter Plot')
        plt.xlabel('Polarity')
        plt.ylabel('Subjectivity(objectivity -> subjectivity)')
        plt.show()

        self.df['Decision'].value_counts().plot(kind='bar')
        plt.title('Decision Analysis Bar Plot')
        plt.xlabel('Decision')
        plt.ylabel('Number of tweets')
        plt.show()

    def predict(self):
        positive = self.df['Decision'].value_counts()['PZ']
        negative = self.df['Decision'].value_counts()['NG']

        maximum = max(positive, negative)
        percent = maximum / (positive + negative)

        if maximum == positive:
            return percent
        else:
            return -1 * percent

    def clean_tweet(self, tweet):
        tweet = re.sub('#' + self.crypto, self.crypto, tweet)
        tweet = re.sub('#' + self.hashtag, self.hashtag, tweet)
        tweet = re.sub("'", "", tweet)
        tweet = re.sub("@[A-Za-z0-9_]+", "", tweet)
        tweet = re.sub("#[A-Za-z0-9_]+", "", tweet)
        tweet = re.sub(r'http\S+', '', tweet)
        tweet = re.sub('\\n', '', tweet)
        return tweet


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags 
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def space(comment):
    global nlp
    doc = nlp(comment)
    return " ".join([token.lemma_ for token in doc])


def get_subjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity


def get_polarity(tweet):
    return TextBlob(tweet).sentiment.polarity


def get_sentiment(score):
    if score <= 0:
        return 'NG'
    else:
        return 'PZ'

