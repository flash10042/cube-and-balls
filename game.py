import pygame
import os
from random import randint
from math import sqrt
import numpy as np
from collections import deque


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cube and Balls")
        self.game_height = 550
        self.game_width = 400
        self.game_display = pygame.display.set_mode((self.game_width, self.game_height))

        self.player = Player(self)
        self.balls, self.ball_x, self.streak = self.create_balls()
        self.score = 0
        self.crash = 0

        # ---- VARS FOR AGENT
        self.observation_space_high = np.array([360, 580, 360, 360, 360])
        self.observation_space_low = np.array([-10, -10, 40, 40, 40])


    def balls_logic(self):
        for b in self.balls:
            b.move()

            self.player_right = self.player.x + self.player.width
            self.player_bottom = self.player.y + self.player.height
            if abs(self.player.y-b.y) <= b.radius:
                if abs(self.player.x-b.x) <= sqrt(b.radius**2 - (self.player.y-b.y)**2) or abs(self.player_right-b.x) <= sqrt(b.radius**2 - (self.player.y-b.y)**2):
                    self.crash = 1
            elif abs(self.player_bottom-b.y) <= b.radius:
                if abs(self.player.x-b.x) <= sqrt(b.radius**2 - (self.player_bottom-b.y)**2) or abs(self.player_right-b.x) <= sqrt(b.radius**2 - (self.player_bottom-b.y)**2):
                    self.crash = 1

        if self.balls[0].y >= 590:
            self.prev_ball_x = self.ball_x
            if not self.streak:
                if self.prev_ball_x == 150:
                    self.ball_x = 50 + 100 * randint(1, 3)
                elif self.prev_ball_x == 250:
                    self.ball_x = 50 + 100 * randint(0, 2)
                else:
                    self.ball_x = 50 + 100 * randint(0, 3)
                if self.ball_x == self.prev_ball_x:
                    self.streak = 1
            else:
                while self.prev_ball_x == self.ball_x:
                    if self.prev_ball_x == 150:
                        self.ball_x = 50 + 100 * randint(1, 3)
                    elif self.prev_ball_x == 250:
                        self.ball_x = 50 + 100 * randint(0, 2)
                    else:
                        self.ball_x = 50 + 100 * randint(0, 3)
                self.streak = 0
            self.balls.append(Ball(self.ball_x, -40))
            self.score += 1


    def balls_displayer(self):
        for b in self.balls:
            b.display_ball(self)


    def display(self):
        self.game_display.fill((255, 255, 255))

        self.player.display_player(self)
        self.balls_displayer()

        self.display_score()

        pygame.display.flip()
        pygame.time.wait(15)


    def display_score(self):
        font = pygame.font.Font(None, 30)
        score_surf = font.render('Score: {}'.format(self.score), True, pygame.Color('black'))
        score_rect = score_surf.get_rect(center=(self.game_width/2, 50))
        self.game_display.blit(score_surf, score_rect)


    def create_balls(self):
        balls = deque(maxlen=7)
        x = 50 #+ 100 * randint(0, 3)
        repeat = 0
        balls.append(Ball(x, 80))
        for i in range(6):
            if not repeat:
                if x == 150:
                    new_x = 50 + 100 * randint(1, 3)
                elif x == 250:
                    new_x = 50 + 100 * randint(0, 2)
                else:
                    new_x = 50 + 100 * randint(0, 3)
                if new_x == x:
                    repeat = 1
            else:
                while x == new_x:
                    if x == 150:
                        new_x = 50 + 100 * randint(1, 3)
                    elif x == 250:
                        new_x = 50 + 100 * randint(0, 2)
                    else:
                        new_x = 50 + 100 * randint(0, 3)
                repeat = 0
            x = new_x
            balls.append(Ball(x, -10-90*i))
        return balls, x, repeat


    def reset(self):
        self.player = Player(self)
        self.balls, self.ball_x, self.streak = self.create_balls()
        self.score = 0
        self.crash = 0

        state = [self.player.x, self.balls[-2].y] + [self.balls[-i].x for i in range(2, 5)]
        return np.array(state)


    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # ------------- ACTIONS -----------------
        # 0 - do nothing 
        # 1 - move left
        # 3 - move up
        # 2 - move right
        # 4 - move down

        reward = 0


        if action == 1 and self.player.x >= 3:
            self.player.x -= 5
            #reward = +.1
        elif action == 3 and self.player.y >= 3:
            self.player.y -= 5
            #reward = +.1
        elif action == 2 and self.player.x <= self.game_width - 3 - self.player.width:
            self.player.x += 5
            #reward = +.1
        elif action == 4 and self.player.y <= self.game_height - 3 - self.player.height:
            self.player.y += 5
            #reward = +.1

        # ----------- MOVE BALLS, CHECK COLLISIONS ----

        self.balls_logic()

        if self.crash:
            reward = -5

        state = [self.player.x, self.balls[1].y] + [self.balls[i].x for i in range(1, 4)]

        return np.array(state), reward, self.crash


    def get_score(self):
        return self.score


class Ball():
    def __init__(self, x, y):
        self.radius = 40
        self.velocity = 4
        self.x = x
        self.y = y


    def move(self):
        self.y += self.velocity


    def display_ball(self, game):
        pygame.draw.circle(game.game_display, (0, 0, 255), (self.x, self.y), self.radius)


class Player(object):
    def __init__(self, game):
        self.x = 175
        self.y = 450
        self.height = 50
        self.width = 50


    def display_player(self, game):
        pygame.draw.rect(game.game_display, (255, 0, 0), (self.x, self.y, self.height, self.width))



def run():
    record = 0

    game = Game()
    game.reset()

    while not game.crash:
        game.display()

        action = 0

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            action = 3
        if pressed[pygame.K_DOWN]:
            action = 4
        if pressed[pygame.K_LEFT]:
            action = 1
        if pressed[pygame.K_RIGHT]:
            action = 2
        game.step(action)




if __name__ == '__main__':
    run()
