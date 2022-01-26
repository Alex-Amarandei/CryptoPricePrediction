import tkinter as tk
from gui import GUI
from theme import DarkTheme
from PIL import Image, ImageTk


def create_root():
    global root
    global theme

    root.title('Your Friendly Neighbourhood Crypto Price Predictor')
    root.iconphoto(True, ImageTk.PhotoImage(file='images/AppIcon.png'))
    root.resizable(False, False)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(str(screen_width) + 'x' + str(screen_height))


if __name__ == '__main__':
    root = tk.Tk()
    theme = DarkTheme

    create_root()
    GUI(root, theme)
    root.mainloop()
