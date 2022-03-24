import pygame as pg
from config import *

vec = pg.math.Vector2

class MayhemSprite(pg.sprite.Sprite):
    def __init__(
            self, 
            groups: pg.sprite.Group, 
            x: int, 
            y: int, 
            w: int, 
            h: int, 
            col=None,
            texture=None
            ):
        super().__init__(groups)
        self.image = pg.Surface((w,h), pg.SRCALPHA)
        if texture is None:
            self.image.fill(col)
        else:
            self.image.blit(texture, (0,0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Player(MayhemSprite):
    def __init__(
            self, 
            game,
            groups: pg.sprite.Group,
            x: int, 
            y: int, 
            w: int, 
            h: int, 
            col: tuple[int, int, int]
            ):

        super().__init__(groups, x, y, w, h, col=col)
        self.game = game
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.controls = None

    def update(self):
        self.acc = vec(0, 0)
        self.keymove()

        # self.acc += vec(0, 10) * 10
        # self.vel += self.acc * self.game.dt
        # self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

    def keymove(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            self.pos[1] -= 5
        if key[pg.K_s]:
            self.pos[1] += 5
        if key[pg.K_a]:
            self.pos[0] -= 5
        if key[pg.K_d]:
            self.pos[0] += 5

class Wall(MayhemSprite):
    def __init__(self, 
            group: pg.sprite.Sprite, 
            x: int, 
            y: int, 
            texture: str
            ):
        super().__init__(group, x, y, TILESIZE, TILESIZE, texture=texture)