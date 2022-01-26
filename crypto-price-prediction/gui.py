import tkinter as tk

from tkinter import *
from PIL import Image, ImageTk
from prediction import PricePredictor


class GUI:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme

        self.background_image = ImageTk.PhotoImage(file=self.theme.background_image_path)
        self.screen = {'width': self.root.winfo_screenwidth(), 'height': self.root.winfo_screenheight()}
        self.main_canvas = tk.Canvas(self.root, width=self.screen['width'], height=self.screen['height'],
                                     cursor='trek')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        self.title = None

        self.ticker_input = None
        self.against_input = None
        self.name_input = None
        self.timeframe_input = None
        self.twitter_options = None
        self.twitter_dropdown = None

        self.ticker_field = None
        self.against_field = None
        self.name_field = None
        self.timeframe_field = None
        self.predict_button = None
        self.twitter_clicked = None

        self.main_canvas.pack(fill='both', expand=True)
        self.main_canvas.bind('<Configure>', self.update)

    def update(self, event):
        self.clean()
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height())
        self.update_fields(event.widget.winfo_width(), event.widget.winfo_height())

    def clean(self):
        self.main_canvas.delete('all')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

    def confirm(self, event):
        self.update(event)

    def update_title(self, width, height, text='Your Friendly Neighbourhood Crypto Price Predictor'):
        font = 'Century ' + str(int(min(width / 32, height / 12))) + ' bold'
        self.title = self.main_canvas.create_text(width / 2,
                                                  height / 10,
                                                  fill=self.theme.font_color,
                                                  font=font,
                                                  text=text)

    def update_fields(self, width, height):
        scale = int(0.02 * width)
        self.ticker_input = tk.Entry(self.root, font=('Helvetica', scale),
                                     width=int(width / 40),
                                     fg='#336d92', bd=0)
        self.ticker_input.insert(2, 'Ticker of the Cryptocurrency')

        self.against_input = tk.Entry(self.root, font=('Helvetica', scale),
                                      width=int(width / 40),
                                      fg='#336d92', bd=0)
        self.against_input.insert(2, 'Currency to measure against')

        self.name_input = tk.Entry(self.root, font=('Helvetica', scale),
                                   width=int(width / 40),
                                   fg='#336d92', bd=0)
        self.name_input.insert(2, 'Name of the Cryptocurrency')

        self.timeframe_input = tk.Entry(self.root, font=('Helvetica', scale),
                                        width=int(width / 40),
                                        fg='#336d92', bd=0)
        self.timeframe_input.insert(2, 'Prediction Timeframe')

        self.twitter_options = ['Last 3 Days', 'Last Week']
        self.twitter_clicked = StringVar()
        self.twitter_clicked.set('Last 3 Days')
        self.twitter_dropdown = OptionMenu(self.root, self.twitter_clicked, *self.twitter_options)
        self.twitter_dropdown.config(font=('Helvetica', scale),
                                     pady=5,
                                     padx=int(width / 7),
                                     fg='#336d92',
                                     bg='#ffffff',
                                     justify='left')
        self.twitter_dropdown.place(relx='0.05',
                                    rely='0.75',
                                    anchor='nw')

        self.ticker_field = self.main_canvas.create_window(width / 4,
                                                           height / 4,
                                                           anchor='center',
                                                           window=self.ticker_input)
        self.against_field = self.main_canvas.create_window(3 * width / 4,
                                                            height / 4,
                                                            anchor='center',
                                                            window=self.against_input)

        self.name_field = self.main_canvas.create_window(width / 4,
                                                         height / 2,
                                                         anchor='center',
                                                         window=self.name_input)
        self.timeframe_field = self.main_canvas.create_window(3 * width / 4,
                                                              height / 2,
                                                              anchor='center',
                                                              window=self.timeframe_input)

        self.predict_button = Button(self.root,
                                     text='Predict',
                                     font=('Helvetica', scale),
                                     pady=5,
                                     padx=int(width / 5.9),
                                     fg='#336d92',
                                     bg='#ffffff',
                                     justify='center',
                                     command=self.predict)
        self.predict_button.place(relx='0.55',
                                  rely='0.75',
                                  anchor='nw')

    def predict(self):
        ticker = self.ticker_input.get()
        against = self.against_input.get()
        name = self.name_input.get()
        timeframe = int(self.timeframe_input.get())
        twitter_timeframe = self.twitter_clicked.get()
        top = Toplevel()
        top.title('Prediction')

        if twitter_timeframe == 'Last Week':
            twitter_timeframe = 168
        else:
            twitter_timeframe = 72

        PricePredictor(top, ticker, against, name, timeframe, twitter_timeframe)
