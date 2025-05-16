import pygame
import sys

class Game:
    @staticmethod
    def sysexit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def init():
        pygame.init()
        pygame.display.set_caption("My Game")
        screen = pygame.display.set_mode((400, 400))
        return screen

Game.init()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            Game.sysexit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.sysexit()