from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import os
from gui.login.login import Login


class Start:

    def __init__(self):
        self.logo_label = None
        self.buttonFrame = None
        self.start_button = None

        self.root = Tk()
        self.root.title('password-manager')
        self.root.geometry('720x520+600+200')
        self.root.resizable(True, True)

        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(fill='both', expand=True)

        self.initLogo()
        self.initButton()

        self.root.mainloop()

    def initLogo(self):
        parent = str(Path(os.getcwd()).parent.parent)
        logo_filename = parent + '/logo/logo.png'
        logo = Image.open(logo_filename)
        logo = logo.resize((280, 280))
        logo = ImageTk.PhotoImage(logo)
        self.logo_label = Label(self.mainFrame, image=logo)
        self.logo_label.image = logo
        self.logo_label.pack()

    def initButton(self):
        self.buttonFrame = Frame(self.mainFrame)

        self.start_button = Button(self.buttonFrame,
                                   text='Iniciar!',
                                   font=('RaleWay', 25),
                                   command=self.start_button_click)
        self.start_button.pack()

        self.buttonFrame.pack(ipady=20, ipadx=20)

    def start_button_click(self):
        for widgets in self.buttonFrame.winfo_children():
            widgets.destroy()

        for widgets in self.mainFrame.winfo_children():
            widgets.destroy()

        self.mainFrame.destroy()

        login = Login(self)


start = Start()