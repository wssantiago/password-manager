from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import os
from login import Login


class Start:

    def __init__(self):
        self.title_label = None
        self.logo_label = None
        self.buttonFrame = None
        self.start_button = None

        self.directory = str(Path(os.getcwd()).parent)

        self.root = Tk()
        self.root.title('password-manager')
        self.root.geometry('720x520+600+200')
        self.root.resizable(True, True)
        self.root.iconbitmap(self.directory + '/images/basketball.ico')

        self.mainFrame = Frame(self.root, bg="#41667f")
        self.mainFrame.pack(fill='both', expand=True)

        self.initLogo()
        self.initButton()

        self.root.mainloop()

    def initLogo(self):
        logo_filename = self.directory + '/images/background.png'
        logo = Image.open(logo_filename)
        logo = logo.resize((280, 280))
        logo = ImageTk.PhotoImage(logo)
        self.logo_label = Label(self.mainFrame, image=logo, bg="#41667f")
        self.logo_label.image = logo
        self.logo_label.pack(side='left', ipadx=50)
        
        self.title_label = Label(self.mainFrame, text="Password \nManager", bg="#41667f", fg="#622323",
                                 font=('Segoe UI', 18, "bold"))
        self.title_label.place(x=155, y=50)

    def initButton(self):
        self.buttonFrame = Frame(self.mainFrame, bg="#41667f")

        self.start_button = Button(self.buttonFrame,
                                   text='Iniciar!',
                                   font=('Segoe UI', 20, "bold"),
                                   command=self.start_button_click, bg="#622323", fg="#ae8349")
        self.start_button.pack(side='right')

        self.buttonFrame.pack(ipady=200)

    def start_button_click(self):
        for widgets in self.buttonFrame.winfo_children():
            widgets.destroy()

        for widgets in self.mainFrame.winfo_children():
            widgets.destroy()

        self.mainFrame.destroy()

        login = Login(self)


start = Start()