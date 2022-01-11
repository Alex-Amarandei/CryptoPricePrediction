from tkinter import *
from PIL import ImageTk, Image
from fetch_period import FetchPeriod as Fp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prediction import PredictionPlot as Pp
from altcoin_names import AltcoinNames as An


def predict():
    crypto = altcoin_clicked.get()
    fiat = fiat_clicked.get()
    twitter = twitter_clicked.get()
    time = int(timeframe_input.get())

    if crypto == 'LTC':
        name = An.LTC
    elif crypto == 'BTC':
        name = An.BTC
    else:
        name = An.ETH

    if twitter == 'Last Week':
        twitter = 168
    else:
        twitter = 72

    Pp(crypto, fiat, time, name, twitter)


def switch_mode():
    global is_advanced
    is_advanced = not is_advanced


if __name__ == '__main__':
    is_advanced = False
    root = Tk()
    root.title('Crypto Price Prediction')
    root.geometry('1200x800')
    root.configure(background='#716b94')

    title = Label(root,
                  text='Your Friendly Neighbourhood Price Predictor',
                  font=('Helvetica', 32),
                  pady=20,
                  bg='#716b94')
    title.pack()

    altcoin_label = Label(root,
                          text='Altcoin:',
                          font=('Helvetica', 24),
                          pady=20,
                          padx=10,
                          bg='#716b94',
                          justify='left')
    altcoin_label.place(relx='0.01',
                        rely='0.1',
                        anchor='nw')

    fiat_label = Label(root,
                       text='Fiat:',
                       font=('Helvetica', 24),
                       pady=20,
                       padx=10,
                       bg='#716b94',
                       justify='left')
    fiat_label.place(relx='0.01',
                     rely='0.2',
                     anchor='nw')

    twitter_label = Label(root,
                          text='Twitter Timeframe:',
                          font=('Helvetica', 24),
                          pady=20,
                          padx=10,
                          bg='#716b94',
                          justify='left')
    twitter_label.place(relx='0.01',
                        rely='0.3',
                        anchor='nw')

    timeframe_label = Label(root,
                            text='Prediction Timeframe:',
                            font=('Helvetica', 24),
                            pady=20,
                            padx=10,
                            bg='#716b94',
                            justify='left')
    timeframe_label.place(relx='0.01',
                          rely='0.4',
                          anchor='nw')

    advanced_button = Button(root,
                             text='Advanced',
                             font=('Helvetica', 24),
                             pady=10,
                             padx=20,
                             bg='#716b94',
                             justify='center',
                             state='disabled',
                             command=switch_mode)
    advanced_button.place(relx='0.025',
                          rely='0.5',
                          anchor='nw')

    predict_button = Button(root,
                            text='Predict',
                            font=('Helvetica', 24),
                            pady=10,
                            padx=20,
                            bg='#716b94',
                            justify='center',
                            command=predict)
    predict_button.place(relx='0.025',
                         rely='0.6',
                         anchor='nw')

    altcoin_clicked = StringVar()
    altcoin_clicked.set('ETH')

    altcoin_options = ['ETH']

    altcoin_dropdown = OptionMenu(root, altcoin_clicked, *altcoin_options)
    altcoin_dropdown.config(font=('Helvetica', 16),
                            pady=10,
                            padx=10,
                            bg='#716b94',
                            justify='left')
    altcoin_dropdown.place(relx='0.15',
                           rely='0.12',
                           anchor='nw')

    fiat_clicked = StringVar()
    fiat_clicked.set('USD')

    fiat_options = ['USD']
    fiat_dropdown = OptionMenu(root, fiat_clicked, *fiat_options)
    fiat_dropdown.config(font=('Helvetica', 16),
                         pady=10,
                         padx=10,
                         bg='#716b94',
                         justify='left')
    fiat_dropdown.place(relx='0.15',
                        rely='0.22',
                        anchor='nw')

    twitter_clicked = StringVar()
    twitter_clicked.set('Last 3 Days')

    twitter_options = ['Last 3 Days', 'Last Week']
    twitter_dropdown = OptionMenu(root, twitter_clicked, *twitter_options)
    twitter_dropdown.config(font=('Helvetica', 16),
                            pady=10,
                            padx=10,
                            bg='#716b94',
                            justify='left', )
    twitter_dropdown.place(relx='0.25',
                           rely='0.32',
                           anchor='nw')

    timeframe_options = ['Last 3 Days', 'Last Week']
    timeframe_input = Entry(root,
                            width=15,
                            borderwidth=2,
                            bg='#978fc7')
    timeframe_input.place(relx='0.25',
                          rely='0.43',
                          anchor='nw')

    root.mainloop()
