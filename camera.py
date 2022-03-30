import pygame as pg
from config import WIDTH, HEIGHT

class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def update(self, *targets):

		centerx = sum([t.rect.centerx for t in targets]) / len(targets)
		centery = sum([t.rect.centery for t in targets]) / len(targets)

		borderleft = centerx - WIDTH // 2
		borderright = centerx + WIDTH // 2
		bordertop = centery - HEIGHT // 2
		borderbottom = centery + HEIGHT // 2

		borderleft = min(0, borderleft)

		# self.camera = pg.Rect(x, y, self.width, self.height)
	
	# def _center_view(self, *targets):
		
		# # center scrolling at the average position of all targets
		# x = -sum([t.x for t in targets]) / len(targets)
		# y = -sum([t.y for t in targets]) / len(targets)

		# # limit scrolling to map size
		# x = min(0, x)
		# y = min(0, y)
		# x = max(-(self.width - WIDTH), x)
		# y = max(-(self.height - HEIGHT), y)

		# return x, y
	
	# def _zoom_view(self, *targets):
		
		# zoom camera such that all targets are in view by adjusting width and height
		
