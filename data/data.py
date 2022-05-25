import sqlite3
import rsa
from pathlib import Path
import os


class Data:

    def __init__(self, path):
        self.path = path + 'pwm.db'
        self.db = None
        self.cursor = None

        self.keys = rsa.newkeys(512)

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

        sqlcmd = 'SELECT *, oid FROM sources WHERE user_login = \'{0}\' AND user_pw = \'{1}\' '.format(user_id[0],
                                                                                                       user_id[1])
        self.cursor.execute(sqlcmd)
        sources = self.cursor.fetchall()

        self.db.commit()
        self.db.close()

        return sources

    def insertUser(self, login, password):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("INSERT INTO users VALUES (:login, :password)",
                            {
                                'login': login,
                                'password': rsa.encrypt(password.encode(), self.keys[0])
                            })

        self.db.commit()
        self.db.close()

    def insertSourceFromUser(self, data, user):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("INSERT INTO sources VALUES (:source, :login, :password, :user_login, :user_pw)",
                            {
                                'source': data[0],
                                'login': data[1],
                                'password': data[2],
                                'user_login': user[0],
                                'user_pw': user[1]
                            })

        self.db.commit()
        self.db.close()

    def deleteUser(self, id):
        self.db = sqlite3.connect(self.path)
        self.cursor = self.db.cursor()

        self.cursor.execute("DELETE FROM users WHERE login = ? AND password = ?", (id[0], id[1]))

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
                            WHERE oid = ?''', (values[0], values[1], values[2], str(oid)))

        self.db.commit()
        self.db.close()


# data = Data('')
# for item in data.getAllSourcesById(('wssf', '1234')):
#    print(item)



