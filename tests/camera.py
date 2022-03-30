import pygame as pg
from settings import WIDTH, HEIGHT

class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, width, height)
		self.width = width
		self.height = height
		self.scale = 1

	def apply(self, entity):
		pg.transform.scale(entity.image, (int(entity.rect.w * self.scale), int(entity.rect.h * self.scale)))
		return entity.rect.move(self.camera.topleft)

	def update(self, target):
		x = -target.rect.x + int(WIDTH / 2)
		y = -target.rect.y + int(HEIGHT / 2)
		# set limits
		x = min(0, x) # left
		y = min(0, y) # top
		x = max(-(self.width - WIDTH), x) # right
		y = max(-(self.height - HEIGHT), y) # bottom

		self.scale = 1

		self.camera = pg.Rect(x, y, self.width, self.height)
