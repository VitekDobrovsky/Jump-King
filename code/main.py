import pygame
from sys import exit
from settings import *
from level import Level

class Game:
    def __init__(self):

        # basic setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        # caption
        icon = pygame.image.load('../graphics/coins/gold/0.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Jump King')

        self.level = Level()

    def run(self):
        while True:

            # exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # drawing
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()