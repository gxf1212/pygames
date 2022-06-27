import random, math, itertools
import matplotlib.pyplot as plt

"""
-1: mine
0: empty
-2: user not opened
"""

LEN_X = 10
LEN_Y = 10
NUM_MINE = 16


def get_neighbor(x, y, LEN_X, LEN_Y):
    xlist = [e for e in [x-1, x, x+1] if 0 <= e < LEN_X]
    ylist = [e for e in [y-1, y, y+1] if 0 <= e < LEN_Y]
    neighbors = list(itertools.product(xlist,ylist))
    neighbors.remove((x,y))
    return neighbors


def generate_game(LEN_X, LEN_Y, NUM_MINE):
    matrix = [[0 for i in range(LEN_X)] for j in range(LEN_Y)]
    rans = random.sample(range(LEN_X*LEN_Y), NUM_MINE)  # no repeat
    # assign mines
    for r in rans:
        matrix[r//LEN_X][r%LEN_X] = -1
    # determine values
    for i,j in itertools.product(range(LEN_X),range(LEN_Y)):
        if matrix[i][j] == -1:
            pass
        else:
            matrix[i][j] = [matrix[a][b] for a,b in get_neighbor(i, j, LEN_X, LEN_Y)].count(-1)
    return matrix


def show_heatmap(matrix):
    fig = plt.figure(figsize=(9.6, 7.2))
    ax = fig.add_subplot(1, 1, 1)
    my_cmap = 'viridis'
    cmap = plt.get_cmap(my_cmap)
    im = plt.imshow(matrix, interpolation='none', cmap=cmap)
    fig.colorbar(im)
    plt.show()


def open(x, y, result, matrix):
    if matrix[x][y] == -1:
        return False


def mine(x, y, result, matrix):
    # mark as mine
    return


def solve_game(matrix):
    result = [[-2 for i in range(len(matrix[0]))] for j in range(len(matrix))]
    while result != matrix:
        if ~open(0, 0, result, matrix):
            print('Game Over!')
            return -1


#%% main
matrix = generate_game(LEN_X, LEN_Y, NUM_MINE)
# show_heatmap(matrix)

# ref: https://blog.csdn.net/Miku_wx/article/details/112215720

#%% version 1
# LEN1 = 10
# LEN2 = 20
# NUM_MINE = 16
# matrix = [[0 for i in range(LEN1)] for j in range(LEN2)]
# rect_x = 200
# rect_y = 200
# while True:
#     clock.tick(5)
#     screen.fill(bg_color)
#     rect_center = pygame.draw.rect(screen, btn_color, [rect_x, rect_y, edgelen, edgelen])
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             pos = pygame.mouse.get_pos()
#             if rect_x-edgelen<pos[0]<rect_x+edgelen and rect_y-edgelen<pos[1]<rect_y+edgelen:
#                 print('a')
#                 flag = True
#
#     if flag:
#         text = self.btn_font.render('1', True, red)
#         text_rect = text.get_rect()
#         text_rect.center = (rect_x+edgelen/2, rect_y+edgelen/2)
#         screen.blit(text, text_rect)
#
#     pygame.display.update()  # no update, no display

#%% trash
# btn_font = pygame.freetype.Font(r"C:\Windows\Fonts\arial.ttf", 24)
# text = btn_font.render_to(screen, (rect_x+edgelen/2, rect_y+edgelen/2), '1')

