import pygame
import sys
import random
import heros
import balls
from math import sqrt

pygame.init()
height, width = 550, 400
win = pygame.display.set_mode((width, height))

pygame.display.set_caption("ITS A FCKING AI!!!")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# ----------- game elements
hero = heros.Hero(175, 450)
ball_pos = 50 + 100 * random.randint(0, 3)
obstacles = [balls.Ball(ball_pos, -40)]
boost = 1
repeat = 0
velocity = 3

# ---------- gen and score
score = 0
gen = 1

score_surf = font.render('Score: {}'.format(score), True, pygame.Color('black'))
score_rect = score_surf.get_rect(center=(width/2, 50))

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((255, 255, 255))

    # --------------BIG BALLS

    if not obstacles == []:
        if obstacles[0].y >= 50:
            score += 1
            old_pos = ball_pos
            if repeat == 0:
                if old_pos == 150:
                    ball_pos = 50 + 100 * random.randint(1, 3)
                elif old_pos == 250:
                    ball_pos = 50 + 100 * random.randint(0, 2)
                else:
                    ball_pos = 50 + 100 * random.randint(0, 3)
                if ball_pos == old_pos:
                    repeat = 1
            else:
                while old_pos == ball_pos:
                    if old_pos == 150:
                        ball_pos = 50 + 100 * random.randint(1, 3)
                    elif old_pos == 250:
                        ball_pos = 50 + 100 * random.randint(0, 2)
                    else:
                        ball_pos = 50 + 100 * random.randint(0, 3)
                repeat = 0
            boost = 1 + (score//10) * 0.1
            velocity = int(3 * boost)
            obstacles.insert(0, balls.Ball(ball_pos, -40))

    for ball in obstacles:
        ball.set_velocity(velocity)

        if ball.y <= 590:
            ball.move()
            ball.draw(win)
        else:
            obstacles.pop(-1)

        left_side = hero.x + hero.width
        if ball.x - 40 <= hero.x <= ball.x + 40:
            if ball.y - sqrt(1600 - (hero.x - ball.x) ** 2) <= hero.y <= ball.y + sqrt(1600 - (hero.x - ball.x) ** 2) or \
                    ball.y - sqrt(1600 - (hero.x - ball.x) ** 2) <= hero.y + hero.height <= \
                    ball.y + sqrt(1600 - (hero.x - ball.x) ** 2):
                ball_pos = 50 + 100 * random.randint(0, 3)
                obstacles = [balls.Ball(ball_pos, -40)]
                hero.x, hero.y = 175, 450
                score = 0
        elif ball.x - 40 <= left_side <= ball.x + 40:
            if ball.y - sqrt(1600 - (left_side - ball.x) ** 2) <= hero.y <= ball.y + sqrt(
                    1600 - (left_side - ball.x) ** 2) \
                    or ball.y - sqrt(1600 - (left_side - ball.x) ** 2) <= hero.y + hero.height <= ball.y + \
                    sqrt(1600 - (left_side - ball.x) ** 2):
                ball_pos = 50 + 100 * random.randint(0, 3)
                obstacles = [balls.Ball(ball_pos, -40)]
                hero.x, hero.y = 175, 450
                score = 0

    # --------------CUBES

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and hero.y >= 3:
        hero.y -= 3
    if pressed[pygame.K_DOWN] and hero.y <= height-3-hero.height:
        hero.y += 3
    if pressed[pygame.K_LEFT] and hero.x >= 3:
        hero.x -= 3
    if pressed[pygame.K_RIGHT] and hero.x <= width-3-hero.width:
        hero.x += 3

    hero.draw(win)

    # --------------SCORE

    score_surf = font.render('Score: {}'.format(score), True, pygame.Color('black'))
    win.blit(score_surf, score_rect)

    pygame.display.flip()
