from pkg_resources import yield_lines
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
		x = -target.rect.x + WIDTH // 4
		y = -target.rect.y + HEIGHT // 4

		x = min(0, x)
		y = min(0, y)
		x = max(-(self.width - WIDTH // 2), x)
		y = max(-(self.height - HEIGHT), y)

		self.camera = pg.Rect(x, y, self.width, self.height)