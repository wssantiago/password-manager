import os
from pathlib import Path
from tkinter import *
from tkinter import ttk
import rsa


class Sources:

    def __init__(self, login, usr):
        self.remove_item_button = None
        self.add_item_button = None
        self.table_scroll = None
        self.cancel_edition_button = None
        self.edit_confirm_button = None
        self.edit_pw_entry = None
        self.edit_login_entry = None
        self.edit_pw_label = None
        self.edit_login_label = None
        self.edit_source_entry = None
        self.edit_source_label = None
        self.editDialog = None
        self.table = None
        self.data_frame = None
        self.searchData = None
        self.searchBox = None
        self.top_frame = None
        self.searchOptions = ["Lugar", "Login/e-mail", "Senha"]
        self.comboSearch = None

        self.directory = str(Path(os.getcwd()).parent)

        privateFile = open(self.directory + "/data/private.txt", "r")
        privateKeyPEM = ''.join([str(item) for item in privateFile.readlines()])
        privateFile.close()
        self.privateKey = rsa.PrivateKey.load_pkcs1(privateKeyPEM.encode('utf-8'))

        publicFile = open(self.directory + "/data/public.txt", "r")
        publicKeyPEM = ''.join([str(item) for item in publicFile.readlines()])
        publicFile.close()
        self.publicKey = rsa.PublicKey.load_pkcs1(publicKeyPEM.encode('utf8'))

        self.root = login.root
        self.mainFrame = Frame(self.root, bg="#41667f")
        self.mainFrame.pack(fill='both', expand=True)

        self.usr = usr
        self.db = login.db
        self.info = self.decryptInfo()

        self.initTopFrame()
        self.initComboBox()
        self.initSearchWidgets()
        self.initCountButtons()
        self.initDataFrame()
        self.initDataTable()

    def decryptInfo(self):
        info = []
        for item in self.getInfo():
            source = rsa.decrypt(item[0], self.privateKey).decode()
            login = rsa.decrypt(item[1], self.privateKey).decode()
            password = rsa.decrypt(item[2], self.privateKey).decode()
            usr_login = item[3]
            usr_pw = item[4]
            info.append((source, login, password, item[3], item[4], item[5]))

        return info

    def getInfo(self):
        return self.db.getAllSourcesById(self.usr)
    # these returns are encrypted ^ \/

    def getInfoByType(self, type):
        return [item[type] for item in self.db.getAllSourcesById(self.usr)]

    def initTopFrame(self):
        self.top_frame = Frame(self.mainFrame, bg="#41667f")
        self.top_frame.pack()

    def initComboBox(self):
        self.comboSearch = ttk.Combobox(self.top_frame, values=self.searchOptions, font=('Segoe UI', 13, "bold"),
                                        background="#a5b1b2", foreground="#622424")
        self.comboSearch.current(0)
        self.comboSearch.grid(row=0, column=0, sticky='sn', padx=10, pady=20)

        # TODO comboSearch.bind

    def initSearchWidgets(self):
        self.searchData = StringVar(self.searchBox)
        self.searchBox = Entry(self.top_frame, font=('Segoe UI', 13, "bold"), textvariable=self.searchData,
                               bg="#a5b1b2", fg="#622424")
        self.searchBox.grid(row=0, column=1, sticky='w', padx=10, pady=20)
        self.searchBox.bind("<KeyRelease>", self.update)

    def initCountButtons(self):
        self.add_item_button = Button(self.top_frame,
                                      text='Adicionar item',
                                      font=('Segoe UI', 10, "bold"), command=self.insertNewEmptySource,
                                      bg="#622323",
                                      fg="#ae8349")
        self.add_item_button.grid(row=0, column=2, padx=10, pady=20)

        self.remove_item_button = Button(self.top_frame,
                                         text='Remover item',
                                         font=('Segoe UI', 10, "bold"), command=self.deleteSourceItem,
                                         bg="#622323",
                                         fg="#ae8349")
        self.remove_item_button.grid(row=0, column=3, padx=10, pady=20)

    def update(self, e):
        searched = self.searchBox.get()
        infoType = self.comboSearch.current()  # 0 = source, 1 = login, 2 = senha

        if searched == "":
            self.initTableItems(self.info)
        else:
            info = []
            for item in self.info:
                if searched.lower() in item[infoType].lower():
                    info.append(item)

            print(info)
            self.initTableItems(info)

    def initDataFrame(self):
        self.data_frame = Frame(self.mainFrame)
        self.data_frame.pack(fill='both', expand=True)

        self.table_scroll = Scrollbar(self.data_frame)
        self.table_scroll.pack(side=RIGHT, fill=Y)

    def initDataTable(self):
        self.table = ttk.Treeview(self.data_frame, selectmode="browse", yscrollcommand=self.table_scroll.set)
        self.table_scroll.config(command=self.table.yview)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#41667f",
                        foreground="black",
                        rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
        style.map('Treeview', background=[('selected', '#287EE2')])

        self.table['columns'] = ("Lugar", "Login/e-mail", "Senha")
        self.table.column('#0', width=0, stretch=NO)
        self.table.column('Lugar', width=120, anchor=W)
        self.table.column('Login/e-mail', width=120, anchor=CENTER)
        self.table.column('Senha', width=120, anchor=W)

        self.table.heading('#0', anchor=W)
        self.table.heading('Lugar', text='Lugar', anchor=W)
        self.table.heading('Login/e-mail', text='Login/e-mail', anchor=CENTER)
        self.table.heading('Senha', text='Senha', anchor=W)

        self.table.tag_configure('oddrow', background='#E4ECF1')
        self.table.tag_configure('evenrow', background="#BCCFDC")

        self.table.bind("<Double-Button-1>", self.editSource)

        self.table.pack(fill='both', expand=True)

        self.initTableItems(self.info)

    def initTableItems(self, info):
        count = len(self.table.get_children())
        for i in range(count):
            self.table.delete(i)

        i = 0
        # info pode ser qualquer lista de tuplas
        for item in info:
            if i % 2 == 0:
                self.table.insert(parent='', index='end',
                                  iid=i, text="Parent",
                                  values=item, tags=('evenrow',))
            else:
                self.table.insert(parent='', index='end',
                                  iid=i, text="Parent",
                                  values=item, tags=('oddrow',))
            i += 1

    def insertNewEmptySource(self):
        try:
            self.db.insertSourceFromUser(("", "", ""), self.usr)
            count = len(self.table.get_children())
            self.table.insert(parent='', index='end',
                              iid=count, text="Parent",
                              values=("", "", ""))

        except FileNotFoundError:
            print('error')

        self.info = self.decryptInfo()
        self.searchBox.delete(0, END)
        self.initTableItems(self.info)

    def deleteSourceItem(self):
        if len(self.table.selection()) == 0:
            return
        else:
            index = self.table.selection()[0]
            oid = self.table.item(index).get('values')[5]

            self.db.deleteSourceFromUser(oid)

            self.info = self.decryptInfo()
            self.searchBox.delete(0, END)
            self.initTableItems(self.info)

    def editSource(self, e):
        index = self.table.selection()[0]
        values = self.table.item(index).get('values')

        self.editDialog = Toplevel(bg="#41667f")
        self.editDialog.grab_set()
        self.editDialog.title('source-edition')
        self.editDialog.geometry('365x200+700+300')
        self.editDialog.resizable(False, False)

        self.edit_source_label = Label(self.editDialog, text='Lugar: ', font=('Segoe UI', 12, "bold"), padx=10, pady=10,
                                       bg="#41667f",
                                       fg="#ae8349", width=10)
        self.edit_source_label.grid(row=0, column=0, sticky='W')

        self.edit_source_entry = Entry(self.editDialog, font=('Segoe UI', 12, "bold"), bg="#a5b1b2", fg="#622424",
                                       width=20)
        self.edit_source_entry.insert(0, values[0])
        self.edit_source_entry.grid(row=0, column=1)

        self.edit_login_label = Label(self.editDialog, text='Login: ', font=('Segoe UI', 12, "bold"), padx=10, pady=10,
                                      bg="#41667f",
                                      fg="#ae8349", width=10)
        self.edit_login_label.grid(row=1, column=0, sticky='W')

        self.edit_login_entry = Entry(self.editDialog, font=('Segoe UI', 12, "bold"), bg="#a5b1b2", fg="#622424",
                                      width=20)
        self.edit_login_entry.insert(0, values[1])
        self.edit_login_entry.grid(row=1, column=1)

        self.edit_pw_label = Label(self.editDialog, text='Senha: ', font=('Segoe UI', 12, "bold"), padx=10, pady=10,
                                   bg="#41667f",
                                   fg="#ae8349", width=10)
        self.edit_pw_label.grid(row=2, column=0, sticky='W')

        self.edit_pw_entry = Entry(self.editDialog, font=('Segoe UI', 12, "bold"), bg="#a5b1b2", fg="#622424",
                                   width=20)
        self.edit_pw_entry.insert(0, values[2])
        self.edit_pw_entry.grid(row=2, column=1)

        self.edit_confirm_button = Button(self.editDialog,
                                          text='Confirmar',
                                          font=('Segoe UI', 10, "bold"), command=self.confirmSourceEdition,
                                          bg="#622323",
                                          fg="#ae8349")
        self.edit_confirm_button.grid(row=3, column=0, sticky='E', padx=15, pady=15)

        self.cancel_edition_button = Button(self.editDialog,
                                            text='Cancelar',
                                            font=('Segoe UI', 10, "bold"), command=lambda: self.editDialog.destroy(),
                                            bg="#622323",
                                            fg="#ae8349")
        self.cancel_edition_button.grid(row=3, column=1, sticky='W', padx=10, pady=15)

    def confirmSourceEdition(self):
        index = self.table.selection()[0]
        values = self.table.item(index).get('values')
        oid = values[5]

        self.db.updateSourceFromUser((self.edit_source_entry.get(),
                                      self.edit_login_entry.get(),
                                      self.edit_pw_entry.get()),
                                     oid)

        self.table.item(index, values=(self.edit_source_entry.get(),
                                       self.edit_login_entry.get(),
                                       self.edit_pw_entry.get(),
                                       values[3],
                                       values[4],
                                       values[5]))

        self.info = self.decryptInfo()

        self.editDialog.destroy()
