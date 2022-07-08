import numpy as np
from enum import Enum

# constants: colors
# pure
white = np.array([255,255,255])
black = (0,0,0)
edgegrey = np.array([5.1,5.1,5.1])*20
yellow = (255,255,0)
red = (255,0,0)
blue = (0,0,255)

yellowfill = (255,230,153)
lightgreenbg = np.array([248,251,246])
lightgreenfill = np.array([226,239,218])
lemonfill = (255,250,205)
lightredfill = (255,199,206)
lightcyanfill = (151,255,255)
lightskyblue = (176,226,255)
brick = (236,222,181)
thistle = (255,225,255)

greenfill = (146,208,80)
bluefill = (155,194,230)

magenta = (255,0,255)
darkred = (139,0,0)
darkblue = (0,0,139)
chocolate = (139,69,19)
navyblue = (0,0,128)
darkorchid = (104,34,139)


class Status(Enum):
    hide = -3  # 0,1,-1
    empty = 0  # not mine
    open = 1   # both open and empty include 0
    boom = -1  # hide or exploded mines
    mark = -2


class ColorTheme(object):
    def light_theme(self):
        btn_color = {0: black,  # whatever
                     1: magenta,
                     2: darkred,
                     3: darkblue,
                     4: black,
                     5: darkorchid,
                     6: magenta,
                     7: navyblue,
                     8: black,
                     9: black}
        btn_bg_other = {Status.hide: white,
                        Status.mark: yellowfill,
                        Status.boom: red}
        btn_bg_color = {0: lightgreenfill,
                        1: lemonfill,
                        2: lightcyanfill,
                        3: lightredfill,
                        4: greenfill,
                        5: lightskyblue,
                        6: yellowfill,
                        7: thistle,
                        8: yellow,
                        9: brick}
        themefile = './resources/light.json'
        return btn_color, btn_bg_other, btn_bg_color, themefile

    def star_theme(self):
        btn_color = {0: black,  # whatever
                     1: magenta,
                     2: darkred,
                     3: darkblue,
                     4: black,
                     5: darkorchid,
                     6: magenta,
                     7: navyblue,
                     8: black,
                     9: black}
        btn_bg_other = {Status.hide: white,
                        Status.mark: yellowfill,
                        Status.boom: red}
        btn_bg_color = {0: lightgreenfill,
                        1: lemonfill,
                        2: lightcyanfill,
                        3: lightredfill,
                        4: greenfill,
                        5: lightskyblue,
                        6: yellowfill,
                        7: thistle,
                        8: yellow,
                        9: brick}
        themefile = './resources/dark.json'
        return btn_color, btn_bg_other, btn_bg_color, themefile

