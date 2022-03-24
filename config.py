import pygame as pg

# GENERAL SETTINGS
FPS = 100
BACKGROUND_COLOR = (50, 50, 50)
TILESIZE = 32
WIDTH, HEIGHT = TILESIZE * 22, TILESIZE * 28

NICE_COL = (255, 182, 193)

# SPRITE SETTINGS
SPRITE_SPEED = 5

MOVE_MAP = {pg.K_a: pg.math.Vector2(-SPRITE_SPEED, 0),
            pg.K_d: pg.math.Vector2(SPRITE_SPEED, 0),
            pg.K_w: pg.math.Vector2(0, -SPRITE_SPEED),
            pg.K_s: pg.math.Vector2(0, SPRITE_SPEED)}
