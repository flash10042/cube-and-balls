import pygame


class Ball:
    radius = 40
    velocity = 3

    def __init__(self, x, y, boost=1):
        self.x = x
        self.y = y
        self.velocity = int(self.velocity * boost)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), self.radius)

    def move(self):
        self.y += self.velocity
