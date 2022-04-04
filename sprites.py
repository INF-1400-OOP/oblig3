import pygame as pg
import numpy as np
from config import *
from game_base_module.settings import *
from game_base_module import map_val

vec = pg.math.Vector2

class MayhemSprite(pg.sprite.Sprite):
    def __init__(
            self,
            groups: pg.sprite.Group,
            x: int,
            y: int,
            w: int,
            h: int,
            texture=None
            ):
        super().__init__(groups)
        self.image = texture
        self.texture = texture
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Wall(MayhemSprite):
    def __init__(self,
            group: pg.sprite.Sprite,
            x: int,
            y: int,
            texture: str,
            texture_id: str,
            ):
        super().__init__(group, x, y, TILESIZE, TILESIZE, texture=texture)
        self.texture_id = texture_id

class FuelTank(pg.sprite.Sprite):
    def __init__(self, player):
        super().__init__(player.game.all_statuses)
        w, h = 100, 20
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=vec(player.screen.rect.topleft) + vec(100, 40))
        self.image.fill(RED)
        self.amount_surf = pg.Surface((w, h), pg.SRCALPHA)
        self.amount_rect = self.amount_surf.get_rect(topleft=self.rect.topleft)
        self.amount_surf.fill(GREEN)
        self.amount = 1000
        self.prev_amount = self.amount

    def update(self):
        if self.amount >= 0:
            self.amount_rect.width = map_val(self.amount, 0, 1000, 0, self.rect.width)
            self.amount_surf = pg.transform.scale(self.amount_surf, self.amount_rect.size)
            self.image.fill(RED)
            self.image.blit(self.amount_surf, (0, 0))

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)
