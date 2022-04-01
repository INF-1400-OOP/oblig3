import pygame as pg
from config import WIDTH, HEIGHT

class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, rect):
		return rect.move(self.camera.topleft)

	def update(self, target):
		# x = -sum([t.rect.centerx for t in targets]) // len(targets) + WIDTH // 2
		# y = -sum([t.rect.centery for t in targets]) // len(targets) + HEIGHT // 2
		x = -target.rect.centerx + WIDTH // 2
		y = -target.rect.centery + HEIGHT // 2

		x = min(0, x)
		y = min(0, y)
		x = max(-(self.width - WIDTH), x)
		y = max(-(self.height - HEIGHT), y)

		self.camera = pg.Rect(x, y, self.width, self.height)