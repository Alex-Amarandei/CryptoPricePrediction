# imports
import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM


class Analyzer:
    def __init__(self, crypto, against, timeframe):
        self.crypto = crypto
        self.against = against
        self.timeframe = timeframe
        self.feed_frame = 120

        self.start = dt.datetime(2017, 1, 1)
        self.end = dt.datetime.now()

        data = web.DataReader(f'{self.crypto}-{self.against}', 'yahoo', self.start, self.end)
        # Data Preparation for Neutral Network
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = self.scaler.fit_transform(data['Adj Close'].values.reshape(-1, 1))

        x_train, y_train = [], []

        for x in range(self.feed_frame, len(scaled_data) - self.timeframe):
            x_train.append(scaled_data[x - self.feed_frame:x, 0])
            y_train.append(scaled_data[x + self.timeframe, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # The Neural Network
        self.model = Sequential()

        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=1))

        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(x_train, y_train, epochs=25, batch_size=32)

        # Testing

        test_start = dt.datetime(2021, 8, 1)
        test_end = dt.datetime.now()

        test_data = web.DataReader(f'{self.crypto}-{self.against}', 'yahoo', test_start, test_end)
        self.actual_prices = test_data['Adj Close'].values

        total_dataset = pd.concat((data['Adj Close'], test_data['Adj Close']), axis=0)

        self.model_inputs = total_dataset[len(total_dataset) - len(test_data) - self.feed_frame:].values.reshape(-1, 1)
        self.model_inputs = self.scaler.fit_transform(self.model_inputs)

        x_test = []

        for x in range(self.feed_frame, len(self.model_inputs)):
            x_test.append(self.model_inputs[x - self.feed_frame:x, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        self.prediction_prices = self.model.predict(x_test)
        self.prediction_prices = self.scaler.inverse_transform(self.prediction_prices)

    def plot(self, sentiment=0, rsi=0, mamacd=0):
        for i in range(0, len(self.prediction_prices)):
            self.prediction_prices[i] += (0.2 * self.prediction_prices[i] * sentiment) + (0.2 * self.prediction_prices[i] * rsi) + (0.2 * self.prediction_prices[i] * mamacd)

        # plt.plot(self.actual_prices, color='black', label='Actual Prices')
        plt.plot(self.prediction_prices, color='green', label='Predicted Prices')
        plt.title(f'{self.crypto} price prediction')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend('upper left')
        plt.show()

