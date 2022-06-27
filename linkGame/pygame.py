import pygame, sys, os

# global variables
os.chdir('./try')
# font = pygame.font.SysFont(pygame.font.get_default_font(), 24)
font = pygame.font.SysFont('didot.ttc', 72)


class Button(object):
    def __init__(self, screen, center, text, color='black'):
        """
        :param center: (self.x, self.y)
        """
        self.center = center
        self.surface = font.render(text, True, color)
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.surface, self.center)
        return

    def click(self):
        return


# 先做个首页熟悉一下
class Game(object):
    # in charge of the first window
    def __init__(self):
        pygame.init()
        size = width, height = 640, 480
        screen = pygame.display.set_mode(size)
        color = (0, 0, 0)
        ball = pygame.image.load('test.png')
        ballrect = ball.get_rect()
        start_button = Button(screen, (width/2, height/2), 'start')

        screen.blit(ball, ballrect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()


# 单局的
class Single(object):
    def __init__(self):
        pygame.init()
        size = width, height = 640, 480
        screen = pygame.display.set_mode(size)
        color = (0, 0, 0)
        ball = pygame.image.load('test.png')
        ballrect = ball.get_rect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.blit(ball, ballrect)
            pygame.display.flip()


#%% main
# Single()
Game()

