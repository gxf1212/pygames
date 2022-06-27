import numpy as np

import tkinter as tk
# from utils import *


# global
TOTAL_WIDTH = 640
TOTAL_HEIGHT = 480
GAME_WIDTH = 600
GAME_HEIGHT = 450


def make_window(title):
    window = tk.Tk()
    window.title(title)
    screenwidth, screenheight = window.winfo_screenwidth(), window.winfo_screenheight()
    size = '%dx%d+%d+%d' % (TOTAL_WIDTH, TOTAL_HEIGHT, (screenwidth - TOTAL_WIDTH) / 2, (screenheight - TOTAL_HEIGHT) / 2)  # center
    # size = '%dx%d' % (TOTAL_WIDTH, TOTAL_HEIGHT)
    window.geometry(size)
    return window


# whole game
class Game(object):
    # the first window
    def __init__(self):
        self.main = make_window('连连看')
        # self.frm = tk.Frame(master=self.main, width=self.main.winfo_screenwidth(),
        #                     height=self.main.winfo_screenheight())
        # self.frm.pack()
        self.__make_button__()
        # 进入消息循环, open window
        self.main.mainloop()

    def __make_button__(self):
        self.start_button = tk.Button(
            # master=self.frm,
            # weight=10, height=5,
            text="LET'S PLAY!",
            bg="blue",  # background
            fg="yellow",  # text
            font='Arial 20 bold',
            # command=self._newgame(),
        )
        self.start_button.place(relx=0.1, rely=0.6)  # add to window, to get property
        self.start_button.update()
        relx = (1 - self.start_button.winfo_width() / self.main.winfo_width()) / 2
        # print(relx)
        # print(self.start_button.winfo_width())
        # print(self.main.winfo_width())
        # print(self.start_button.winfo_x())
        self.start_button.place(relx=relx, rely=0.6)
        self.start_button.bind("<Button-1>", newgame)


# single game
class Single(object):
    def __init__(self):
        self.main = make_window('第一关')
        #TODO:做游戏的panel


# utils
def newgame(self):
    game2 = Single()
    return 0


def generate_minefield(x, y, m):
    """
    #x, y: size of the field
    #m: number of mines
    #return: a matrix. 0 means empty, -1 means a mine, natural numbers means ...
    """
    field = np.zeros(shape=(x,y), dtype=int)
    return field


#%% main
game = Game()


