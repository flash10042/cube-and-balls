import pygame
import os
from random import randint
from math import sqrt


class Game:
	def __init__(self):
		pygame.display.set_caption("Cube and Balls")
		self.game_height = 550
		self.game_width = 400
		self.game_display = pygame.display.set_mode((self.game_width, self.game_height))

		self.player = Player(self)
		self.balls = [Ball(50 + 100 * randint(0, 3), -40, self)]
		self.score = 0
		self.crash = 0

		# ---- Fields for balls generator
		self.ball_x = self.balls[0].x
		self.streak = 0


	def balls_logic(self):
		for b in self.balls:
			b.move()

			if b.y >= 590:
				self.balls.pop(-1)

			self.player_right = self.player.x + self.player.width
			self.player_bottom = self.player.y + self.player.height
			if abs(self.player.x-b.x) <= b.radius:
				if abs(self.player.y-b.y) <= sqrt(b.radius**2 - (self.player.x-b.x)**2) or abs(self.player_bottom-b.y) <= sqrt(b.radius**2 - (self.player.x-b.x)**2):
					self.crash = 1
			elif abs(self.player_right-b.x) <= b.radius:
				if abs(self.player.y-b.y) <= sqrt(b.radius**2 - (self.player_right-b.x)**2) or abs(self.player_bottom-b.y) <= sqrt(b.radius**2 - (self.player_right-b.x)**2):
					self.crash = 1


		if self.balls:
			if self.balls[0].y >= 50:
				self.score += 1
				self.prev_ball_x = self.ball_x
				if self.streak == 0:
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
				self.balls.insert(0, Ball(self.ball_x, -40, self))


	def balls_displayer(self):
		for b in self.balls:
			b.display_ball(self)


class Ball():
	def __init__(self, x, y, game):
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


	def move(self, action, game):
		# ------------- ACTIONS -----------------
		# 0 - do nothing 
		# 1 - move left
		# 2 - move up
		# 3 - move right
		# 4 - move down

		if action == 1 and self.x >= 3:
			self.x -= 5
		elif action == 2 and self.y >= 3:
			self.y -= 5
		elif action == 3 and self.x <= game.game_width - 3 - self.width:
			self.x += 5
		elif action == 4 and self.y <= game.game_height - 3 - self.height:
			self.y += 5

		# ----------- MOVE BALLS, CHECK COLLISIONS ----

		game.balls_logic()


	def display_player(self, game):
		pygame.draw.rect(game.game_display, (255, 0, 0), (self.x, self.y, self.height, self.width))


def display(game, player):
	game.game_display.fill((255, 255, 255))

	player.display_player(game)
	game.balls_displayer()

	display_score(game)

	pygame.display.flip()


def display_score(game):
	font = pygame.font.Font(None, 30)
	score_surf = font.render('Score: {}'.format(game.score), True, pygame.Color('black'))
	score_rect = score_surf.get_rect(center=(game.game_width/2, 50))
	game.game_display.blit(score_surf, score_rect)


def run():
	pygame.init()
	record = 0

	game = Game()

	while not game.crash:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		display(game, game.player)
		pygame.time.wait(15)

		action = 0

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_UP]:
			action = 2
		if pressed[pygame.K_DOWN]:
			action = 4
		if pressed[pygame.K_LEFT]:
			action = 1
		if pressed[pygame.K_RIGHT]:
			action = 3
		game.player.move(action, game)




if __name__ == '__main__':
	run()
