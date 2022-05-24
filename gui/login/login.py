from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import os
from data.data import Data
from gui.sources.sources import Sources


class Login:

    def __init__(self, start):
        self.user_added_success = None
        self.password_data = None
        self.login_data = None
        self.logo_label = None
        self.loginFrame = None
        self.login_text = None
        self.login_input = None
        self.password_text = None
        self.password_input = None
        self.buttonsFrame = None
        self.confirm_button = None
        self.addUser_button = None

        self.db = Data(str(Path(os.getcwd()).parent.parent) + '/data/')
        self.users = self.db.getUsers()

        self.root = start.root

        self.mainFrame = Frame(self.root, bg="#41667f")
        self.mainFrame.pack(fill='both', expand=True)

        self.initLogo()
        self.initData()
        self.initButtons()

        self.root.mainloop()

    def initLogo(self):
        parent = str(Path(os.getcwd()).parent.parent)
        logo_filename = parent + '/images/logo.png'
        logo = Image.open(logo_filename)
        logo = logo.resize((280, 280))
        logo = ImageTk.PhotoImage(logo)
        self.logo_label = Label(self.mainFrame, image=logo, bg="#41667f")
        self.logo_label.image = logo
        self.logo_label.pack()

    def initData(self):
        self.loginFrame = Frame(self.mainFrame, bg="#41667f")

        self.login_text = Label(self.loginFrame, text='Login: ', font=('Segoe UI', 18, "bold"), padx=7, pady=18,
                                bg="#41667f", fg="#ae8349")
        self.login_text.grid(row=0, column=0, sticky='W')

        self.login_data = StringVar(self.login_input)
        self.login_data.trace('w', self.account_modified)
        self.login_input = Entry(self.loginFrame, font=('Segoe UI', 18, "bold"), textvariable=self.login_data,
                                 bg="#a5b1b2", fg="#622424")
        self.login_input.grid(row=0, column=1)

        self.password_text = Label(self.loginFrame, text='Senha: ', font=('Segoe UI', 18, "bold"), padx=7, pady=18,
                                   bg="#41667f", fg="#ae8349")
        self.password_text.grid(row=1, column=0, sticky='W')

        self.password_data = StringVar(self.password_input)
        self.password_data.trace('w', self.account_modified)
        self.password_input = Entry(self.loginFrame, font=('Segoe UI', 18, "bold"), textvariable=self.password_data,
                                    bg="#a5b1b2", fg="#622424")
        self.password_input.grid(row=1, column=1)

        self.loginFrame.pack()

    def initButtons(self):
        self.buttonsFrame = Frame(self.mainFrame, bg="#41667f")

        self.confirm_button = Button(self.buttonsFrame,
                                     text='Confirmar',
                                     font=('Segoe UI', 18, "bold"),
                                     state=DISABLED,
                                     command=self.login,
                                     bg="#622323",
                                     fg="#ae8349")
        self.confirm_button.pack(side='right')
        self.addUser_button = Button(self.buttonsFrame,
                                     text='Adicionar usuário',
                                     font=('Segoe UI', 18, "bold"),
                                     state=DISABLED,
                                     command=self.addUser,
                                     bg="#622323",
                                     fg="#ae8349")
        self.addUser_button.pack(side='left')

        self.buttonsFrame.pack(ipady=18, ipadx=18)

    def account_modified(self, *args):
        if not self.login_data.get() or not self.password_data.get():
            self.confirm_button['state'] = DISABLED
            self.addUser_button['state'] = DISABLED

        else:
            login_data = self.login_data.get()
            password_data = self.password_data.get()
            for user in self.users:
                login, pw, oid = user
                if login != login_data or pw != password_data:
                    self.confirm_button['state'] = DISABLED
                    self.addUser_button['state'] = ACTIVE
                else:
                    self.confirm_button['state'] = ACTIVE
                    self.addUser_button['state'] = DISABLED


    def addUser(self):
        self.db.insertUser(self.login_data.get(), self.password_data.get())

        # TODO adicionar aviso de que usuario foi adicionado
        # self.user_added_success.config(text="Usuário '{0}' adicionado com sucesso!".format(self.login_data.get()))
        self.login_data.set('')
        self.password_data.set('')
        self.users = self.db.getUsers()

    def login(self):
        self.confirm_button.config(text='Entrando...')
        usr = (self.login_data.get(), self.password_data.get())
        self.destroy()
        sources = Sources(self, usr)

    def destroy(self):
        for widget in self.loginFrame.winfo_children():
            widget.destroy()
        for widget in self.buttonsFrame.winfo_children():
            widget.destroy()
        self.loginFrame.destroy()
        self.buttonsFrame.destroy()
        self.logo_label.destroy()
        self.mainFrame.destroy()
