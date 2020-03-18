import pygame


class Hero:
    height = 50
    width = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.height, self.width))
