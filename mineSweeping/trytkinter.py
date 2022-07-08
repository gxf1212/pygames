import tkinter as tk
from utils import *
import time, copy
import math, random, itertools
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


themechooser = ColorTheme()
btn_color, btn_bg_other, btn_bg_color, themefile = themechooser.light_theme()


class Box(object):
    def __init__(self, value, i, j):
        self.value = value
        self.i = i
        self.j = j
        self.status = Status.hide

    def get_btn_text(self):
        btn_text = {Status.hide: '',
                    Status.empty: '',
                    Status.open: str(self.value),  # empty or open
                    Status.mark: '🚩',             # triangular_flag_on_post
                    Status.boom: '💣'}
        return btn_text[self.status]
        # not useful: return fa.icons['bomb']  # flag icon? fa.icons['flag']

    def get_btn_color(self):
        if self.value < 0:
            return black
        else:
            return btn_color[self.value]

    def get_btn_bg_color(self):
        if self.status == Status.empty or self.status == Status.open:
            return btn_bg_color[self.value]
        else:
            return btn_bg_other[self.status]


def get_neighbor(i, j, LEN1, LEN2):
    ilist = [e for e in [i-1, i, i+1] if 0 <= e < LEN1]
    jlist = [e for e in [j-1, j, j+1] if 0 <= e < LEN2]
    neighbors = list(itertools.product(ilist,jlist))
    neighbors.remove((i,j))
    return neighbors


def generate_game(LEN1, LEN2, NUM_MINE):
    matrix = [[0 for i in range(LEN2)] for j in range(LEN1)]  # numbers
    board = copy.deepcopy(matrix)
    # assign mines
    rans = random.sample(range(LEN1*LEN2), NUM_MINE)  # no repeat!
    for r in rans:
        matrix[r//LEN2][r%LEN2] = -1
    # determine values
    for i,j in itertools.product(range(LEN1),range(LEN2)):
        if matrix[i][j] != -1:
            matrix[i][j] = [matrix[a][b] for a,b in get_neighbor(i, j, LEN1, LEN2)].count(-1)
        board[i][j] = Box(matrix[i][j], i, j)
    return board


TOTAL_WIDTH = 640
TOTAL_HEIGHT = 480


class Start(object):
    # the first window
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('扫雷')
        screenwidth, screenheight = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        size = '%dx%d+%d+%d' % (TOTAL_WIDTH, TOTAL_HEIGHT,
                    (screenwidth - TOTAL_WIDTH) / 2, (screenheight - TOTAL_HEIGHT) / 2)  # size, center
        self.window.geometry(size)
        self.__make_first_button__()
        self.window.mainloop()  # enter mainloop: open window

    def __make_first_button__(self):
        self.start_button = tk.Button(
            text="LET'S PLAY!",
            bg="blue",  # background
            fg="yellow",  # text
            font='Arial 20 bold',
        )
        self.start_button.place(relx=0.1, rely=0.6)  # add to window, wherever, to get property
        self.start_button.update()
        relx = (1 - self.start_button.winfo_width() / self.window.winfo_width()) / 2
        self.start_button.place(relx=relx, rely=0.6)
        self.start_button.bind("<Button-1>", self.newgame)

    def newgame(self, event, len1=10, len2=10):
        game = Game(self.window, len1, len2, 20)


class GameStatus(Enum):
    normal = 0
    game_over = -1
    pause = 2
    win = 1


EDGE = 30
TOOL = 200


class Game(object):
    def __init__(self, window, LEN1, LEN2, NUM_MINES):
        self.LEN1 = LEN1
        self.LEN2 = LEN2
        self.NUM_MINES = NUM_MINES
        self.window = window
        # calculate size params
        self.screen_height = min(max(360,180+LEN2*18), 630)         # 360~630(after 20)
        self.edgelen = (self.screen_height-2*EDGE)/LEN2             # evenly divide
        self.screen_width = int(max(self.screen_height*4/3,
                                    EDGE+LEN1*self.edgelen+TOOL))   # 4:3, but in case larger LENX..
        size = '%dx%d+%d+%d' % (self.screen_width, self.screen_height,
                                (self.window.winfo_screenwidth()-self.screen_width)/2,
                                (self.window.winfo_screenheight()-self.screen_height)/2)
        self.window.geometry(size)
        self.board = generate_game(self.LEN1, self.LEN2, self.NUM_MINES)
        # other
        # self.btn_font_size = int(0.75*self.edgelen)  # proportional
        self.status = GameStatus.normal  # whatever

    def draw_board(self):
        # draw rectangles, edges and texts (with proper color)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                pass





#%% main
start = Start()

