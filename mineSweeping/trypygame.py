from utils import *
import pygame
import time,copy
import math,random,itertools
import pandas as pd
import matplotlib.pyplot as plt
import fontawesome as fa  # still does not work
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.windows import *
# from pygame_gui.windows.ui_console_window import *
#TODO:进阶，优化get set
#TODO:merge empty and normal


themechooser = ColorTheme()
btn_color, btn_bg_other, btn_bg_color, themefile = themechooser.light_theme()


class Button(object):
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
        board[i][j] = Button(matrix[i][j], i, j)
    return board


def add_text(screen, font, text, pos, color):
    text = font.render(text, True, color)
    text_rect = text.get_rect()  # position
    text_rect.center = pos
    screen.blit(text, text_rect)


class MessageWindow(UIMessageWindow):
    def __init__(self, rect, html_message, manager, window_title, visible):
        super().__init__(rect=rect,
                         html_message=html_message,
                         manager=manager,
                         window_title=window_title,
                         visible=visible)
        self.anchors['right'] = 'bottom'
        self.anchors['bottom'] = 'bottom'
        self.dismiss_button.text = 'OK'

    def enableshow(self):
        # super().enable()
        super().show()
        # self.visible = 1
        # self.title_bar.visible = 1
        # self.dismiss_button.visible = 1
        # self.window_element_container.visible = 1
        # self._window_root_container.visible = 1


class GameStatus(Enum):
    normal = 0
    game_over = -1
    pause = 2
    win = 1


EDGE = 30
TOOL = 200
clock = pygame.time.Clock()


class Game(object):
    # in charge of the first window
    def __init__(self, LEN1, LEN2, NUM_MINES):
        # the board is in the left upper panel, with EDGE carefully calculated
        self.LEN1 = LEN1
        self.LEN2 = LEN2
        self.NUM_MINES = NUM_MINES
        self.screen_height = min(max(360,180+LEN2*18), 630)  # 360~540(after 20)
        self.edgelen = (self.screen_height-2*EDGE)/LEN2  # evenly divide
        self.screen_width = int(max(self.screen_height*4/3, EDGE+LEN1*self.edgelen+TOOL))  # 4:3, but in case larger LENX..
        self.btn_font_size = int(0.75*self.edgelen)  # proportional
        self.status = GameStatus.normal  # whatever
        # others, just define...
        self.result_font_size = int(self.screen_height/6)
        self.game_font_size = int(self.screen_height/20)
        self.screen = self.btn_font = self.game_font = self.result_font = None
        self.manager = self.dt = self.newgame_button = self.result_dialog = None
        self.count_hide = 0
        self.count_mark = 0

    def get_matrix(self):
        # extract values from each element
        # board is a nested list, matrix is a dataframe
        return pd.DataFrame(self.board).applymap(lambda x: x.value)

    def show_heatmap(self):
        # an overview of the board, data analysis
        fig = plt.figure(figsize=(9.6, 7.2))
        ax = fig.add_subplot(1, 1, 1)
        my_cmap = 'viridis'
        cmap = plt.get_cmap(my_cmap)
        im = plt.imshow(self.get_matrix(), interpolation='none', cmap=cmap)
        fig.colorbar(im)
        plt.show()

    def left_click_button(self, button):
        if button.value == -1:  # is mine
            self.status = GameStatus.game_over
            button.status = Status.boom
        else:  # not mine
            self.open_button(button)
        return True

    def right_click_button(self, button):
        self.count()
        if self.count_mark >= self.NUM_MINES:
            self.over_mine()
        else:
            if button.status == Status.hide:
                button.status = Status.mark
            elif button.status == Status.mark:  # switch to another
                button.status = Status.hide

    def open_button(self, button):
        # normal, open itself
        if button.value > 0:
            button.status = Status.open
        elif button.value == 0:
            # 0, empty. there must be no mines around. open all neighbors
            button.status = Status.empty
            for i,j in get_neighbor(button.i, button.j, self.LEN1, self.LEN2):
                btn = self.board[i][j]  # either open or hide
                if btn.status == Status.hide:
                    self.open_button(btn)  # recurrently

    def over_mine(self):
        # mines used up, cannot put a single mine
        self.result_dialog.enableshow()
        self.result_dialog.set_display_title('Warning')
        self.result_dialog.html_message = '<font color=red><strong>不允许标记雷</strong>，因为数量已经超过限制</font>'
        # self.result_dialog.html_message = '<font color=black>不允许标记雷，因为数量已经超过限制</font>'
        # self.result_dialog

    def count(self):
        # count the number of hide and mark, to judge: win or not? add more mines? print # of mines
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                button = self.board[i][j]
                if button.status == Status.hide:
                    self.count_hide += 1
                elif button.status == Status.mark:
                    self.count_mark += 1

    def game_over(self):
        # lose status and dialog params
        self.result_dialog.set_display_title('Message')
        self.result_dialog.html_message = 'Game Over!'
        self.result_dialog.window_display_title = 'Game Over'
        # window_title
        self.result_dialog.visible = 1

    def game_win(self):
        # dialog params
        self.result_dialog.set_display_title('Message')
        self.result_dialog.html_message = 'You Win!'
        self.result_dialog.window_display_title = 'You Win'
        self.result_dialog.visible = 1

    def draw_board(self):
        # draw rectangles, edges and texts (with proper color)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                pygame.draw.rect(self.screen, self.board[i][j].get_btn_bg_color(),
                                 [EDGE + i * self.edgelen, EDGE + j * self.edgelen,
                                  self.edgelen, self.edgelen], width=0)  # fill color
                pygame.draw.rect(self.screen, edgegrey,
                                 [EDGE + i * self.edgelen, EDGE + j * self.edgelen,
                                  self.edgelen, self.edgelen], width=1)  # the frame
                add_text(self.screen, self.btn_font, self.board[i][j].get_btn_text(),
                         (EDGE + (i + 1 / 2) * self.edgelen, EDGE + (j + 1 / 2) * self.edgelen),
                         self.board[i][j].get_btn_color())

    def define_fonts(self):
        # fonts for the board
        self.btn_font = pygame.font.SysFont('Segoe UI Symbol', self.btn_font_size)
        # Font Awesome, Font Awesome 6 Brands, Font Awesome 6 Free
        self.game_font = pygame.font.SysFont('arial', self.btn_font_size)
        self.result_font = pygame.font.SysFont('comicsansms', self.result_font_size)
        # self.what_font = pygame.font.SysFont('arial', self.btn_font_size)
        # Libertinus Serif

    def define_other(self):
        pass

    def draw_screen(self):
        # initialize the screen, draw the basic board, button, etc.
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('扫雷')
        # basic settings
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height),themefile)
        self.define_fonts()             # must, after pygame.init
        self.dt = clock.tick(5)/1000    # 5 cycles a second
        # draw the startup menu
        bg = (white*self.count_hide/self.LEN1/self.LEN2 +
              lightgreenbg*(1-self.count_hide/self.LEN1/self.LEN2))
        self.screen.fill(bg)            # gradual change of background
        # other buttons
        newgame_rect = pygame.Rect(0, 0, 100, 40)
        newgame_rect.topright = (-50, 50)
        self.newgame_button = UIButton(relative_rect=newgame_rect, text='New Game', manager=self.manager,
                                       anchors={'left': 'right',
                                                'right': 'right',
                                                'top': 'top',
                                                'bottom': 'top'})
        result_width = 250
        result_height = 160
        result_rect = pygame.Rect((self.screen.get_rect().width-result_width)/2,
                             (self.screen.get_rect().height-result_height)/2,
                             result_width, result_height)
        self.result_dialog = MessageWindow(rect=result_rect,
                                           html_message='',
                                           manager=self.manager,
                                           window_title='Message',  # 提示
                                           visible=False)
        # the board
        self.draw_board()

    def handle_events(self):
        for event in pygame.event.get():  # normal operation
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and self.status == GameStatus.normal:
                pos = pygame.mouse.get_pos()
                click1 = math.floor((pos[0]-EDGE) / self.edgelen)  # get button index
                click2 = math.floor((pos[1]-EDGE) / self.edgelen)
                if 0 <= click1 < self.LEN1 and 0 <= click2 < self.LEN2:
                    # other position, empty or other, no response
                    button = self.board[click1][click2]
                    # print(button.value)
                    if event.button == 1:  # left click
                        self.left_click_button(button)
                    elif event.button == 3:  # right click
                        self.right_click_button(button)
                    self.count()
                    if self.count_hide == 0 and self.count_mark == self.NUM_MINES:  # number is satisfied, and not boom
                        self.status = GameStatus.win
            # button
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.newgame_button:
                    print('New Game started')
                    # pygame.quit()
                    self.newgame()
                    #TODO: re-generate the matrix, deal with the windows
            # left click other, no response?
            self.manager.process_events(event)
        self.manager.update(self.dt)

    def draw_changes(self):
        if self.status == GameStatus.pause:
            rect = pygame.draw.rect(self.screen, edgegrey, [EDGE, EDGE,
                                    self.edgelen * self.LEN1, self.edgelen * self.LEN2],
                                    width=0)
            add_text(self.screen, self.game_font, 'PAUSED',
                     rect.center, red)
            return
        # normal, over
        # count status
        self.count_hide = 0
        self.count_mark = 0
        # all button, draw and status
        self.draw_board()

        # game status
        if self.status == GameStatus.game_over:  # pop a window
            self.game_over()
        elif self.status == GameStatus.win:
            self.game_win()
        self.manager.draw_ui(self.screen)

    def newgame(self):
        self.board = generate_game(self.LEN1, self.LEN2, self.NUM_MINES)
        self.status = GameStatus.normal
        self.draw_screen()
        while True:
            self.handle_events()        # extract info from events
            self.draw_changes()         # draw the changes
            # in the end. no update, no display
            pygame.display.update()
            time.sleep(0.04)


game = Game(1, 1, 0)
# game = Game(10, 10, 20)
game.newgame()

#%% test
