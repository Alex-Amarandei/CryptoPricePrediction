import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Analyzer:
    def __init__(self, crypto, against, timeframe):
        self.root = None
        self.crypto = crypto
        self.against = against
        self.timeframe = 2 * timeframe

        self.start = dt.datetime(2017, 1, 1)
        self.end = dt.datetime.now() - dt.timedelta(self.timeframe)

        data = web.DataReader(f'{self.crypto}-{self.against}', 'yahoo', self.start, self.end)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = self.scaler.fit_transform(data['Adj Close'].values.reshape(-1, 1))

        x_train, y_train = [], []

        for x in range(self.timeframe, len(scaled_data)):
            x_train.append(scaled_data[x - self.timeframe:x, 0])
            y_train.append(scaled_data[x, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

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

        # save and load model

        test_start = dt.datetime.now() - dt.timedelta(self.timeframe)
        test_end = dt.datetime.now()

        test_data = web.DataReader(f'{self.crypto}-{self.against}', 'yahoo', test_start, test_end)
        self.actual_prices = test_data['Adj Close'].values

        total_dataset = pd.concat((data['Adj Close'], test_data['Adj Close']), axis=0)

        self.model_inputs = total_dataset[len(total_dataset) - len(test_data) - self.timeframe:].values.reshape(-1, 1)
        self.model_inputs = self.scaler.fit_transform(self.model_inputs)

        x_test = []

        for x in range(self.timeframe, len(self.model_inputs)):
            x_test.append(self.model_inputs[x - self.timeframe:x, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        self.prediction_prices = self.model.predict(x_test)
        self.prediction_prices = self.scaler.inverse_transform(self.prediction_prices)

    def plot(self, root, sentiment=0, rsi=0, mamacd=0):
        self.root = root

        for i in range(0, len(self.prediction_prices)):
            self.prediction_prices[i] += (0.2 * self.prediction_prices[i] * sentiment) + (0.25 * self.prediction_prices[i] * rsi) + (0.15 * self.prediction_prices[i] * mamacd)

        plt.plot(self.prediction_prices, color='green', label='Predicted Prices')
        plt.title(f'{self.crypto} price prediction')
        plt.xticks([])
        plt.ylabel('Price')
        plt.show()

        figure = plt.figure(figsize=(15, 10), dpi=100)
        figure.add_subplot(111).plot(self.prediction_prices, color='green', label='Predicted Prices')

        chart = FigureCanvasTkAgg(figure, self.root)
        chart.get_tk_widget().grid(row=0, column=0)

        plt.grid()
