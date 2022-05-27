import sqlite3
import rsa
from pathlib import Path
import os


class Data:

    def __init__(self, path):
        self.path = path + 'pwm.db'
        self.db = None
        self.cursor = None

        publicFile = open(path + "public.txt", "r")
        publicKeyPEM = ''.join([str(item) for item in publicFile.readlines()])
        publicFile.close()
        self.publicKey = rsa.PublicKey.load_pkcs1(publicKeyPEM.encode('utf8'))

        privateFile = open(path + "private.txt", "r")
        privateKeyPEM = ''.join([str(item) for item in privateFile.readlines()])
        privateFile.close()
        self.privateKey = rsa.PrivateKey.load_pkcs1(privateKeyPEM.encode('utf-8'))

    def create_table(self, script):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute(script)

        self.db.commit()
        self.db.close()

    def drop_tables(self):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("DROP TABLE sources")
        self.cursor.execute("DROP TABLE users")

        self.db.commit()
        self.db.close()

    def getUsers(self):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT *, oid FROM users")
        users = self.cursor.fetchall()

        self.db.commit()
        self.db.close()

        return users

    def getUserById(self, id):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT * FROM users"
                            "WHERE login = ? AND password = ?", id[0], id[1])
        user = self.cursor.fetchall()

        self.db.commit()
        self.db.close()

        return user

    def getAllSourcesById(self, user_id):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute('SELECT *, oid FROM sources WHERE user_login = ? AND user_pw = ?',
                            (user_id[0], user_id[1]))
        sources = self.cursor.fetchall()

        self.db.commit()
        self.db.close()

        return sources

    def insertUser(self, login, password):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("INSERT INTO users VALUES (:login, :password)",
                            {
                                'login': rsa.encrypt(str(login).encode(), self.publicKey),
                                'password': rsa.encrypt(str(password).encode(), self.publicKey)
                            })

        self.db.commit()
        self.db.close()

    def insertSourceFromUser(self, data, user):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("INSERT INTO sources VALUES (:source, :login, :password, :user_login, :user_pw)",
                            {
                                'source': rsa.encrypt(str(data[0]).encode(), self.publicKey),
                                'login': rsa.encrypt(str(data[1]).encode(), self.publicKey),
                                'password': rsa.encrypt(str(data[2]).encode(), self.publicKey),
                                'user_login': user[0],
                                'user_pw': user[1]
                            })

        self.db.commit()
        self.db.close()

    # TODO unable to get these users for delete
    def deleteUser(self, id):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("DELETE FROM users WHERE login = ? AND password = ?",
                            (rsa.encrypt(str(id[0]).encode(), self.publicKey),
                             rsa.encrypt(str(id[1]).encode(), self.publicKey)))

        self.db.commit()
        self.db.close()

    def deleteSourceFromUser(self, id):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("DELETE FROM sources WHERE oid=?", (str(id),))

        self.db.commit()
        self.db.close()

    def updateSourceFromUser(self, values, oid):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute('''UPDATE sources
                            SET source = ? ,
                                login = ? ,
                                password = ?
                            WHERE oid = ?''', (rsa.encrypt(str(values[0]).encode(), self.publicKey),
                                               rsa.encrypt(str(values[1]).encode(), self.publicKey),
                                               rsa.encrypt(str(values[2]).encode(), self.publicKey),
                                               str(oid)))

        self.db.commit()
        self.db.close()


#data = Data('')

