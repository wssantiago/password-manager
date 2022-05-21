from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import os
from data.data import Data


class Sources:

    def __init__(self, tk, usr):
        self.root = tk

        self.usr = usr
        self.db = Data(str(Path(os.getcwd()).parent.parent) + '/data/')
        self.info = self.getInfo()

    def getInfo(self):
        return self.db.getAllSourcesById(self.usr)