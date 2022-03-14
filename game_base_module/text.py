import pygame as pg
vec = pg.math.Vector2

pg.font.init()

FONT_TYPE = pg.font.match_font('freesansbold.ttf')

def draw_text(surf, text, size, x, y, color, center=False, font_name=FONT_TYPE):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect() if not center else text_surface.get_rect(center=vec(x, y))
	if not center:
		text_rect = vec(x, y)
	surf.blit(text_surface, text_rect)