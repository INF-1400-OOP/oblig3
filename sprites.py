import pygame as pg
import numpy as np
from config import *
from game_base_module.settings import *

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

class LaserBeam(pg.sprite.Sprite):
    def __init__(self,
            sender,
            game,
            pos: vec, 
            direction: int
            ):
        self.game = game
        self.sender = sender
        super().__init__(game.all_sprites, game.all_projectiles)
        self.pos = pos
        self.dir = direction
        self.image = self.game.laser_img
        self.image, self.rect, self.mask = self.rotate_img(self.image, -self.dir)
        self.vel = vec(0, -PROJECTILE_SPEED).rotate(self.dir)
        self.d_vel = 0.9

    def update(self, *args):
        # self.vel *= self.d_vel * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self._collide()

    def _collide(self):
        for wall in self.game.all_walls:
            if pg.sprite.collide_mask(self, wall):
                self.kill()

    @staticmethod
    def rotate_img(img: pg.Surface, angle: float) -> tuple[pg.Surface, pg.Rect]:
        """ Rotates image by given angle. 
        
        Args:
            img: pygame.Surface
                Original image.
            angle: float
                Angle to be rotated by

        Returns:
            pygame.Surface:
                New rotated image.
            pygame.Rect:
                new rotated (and scaled) rect.
        """

        old_center = img.get_rect().center
        rot_img = pg.transform.rotate(img, angle)
        rot_img.set_colorkey(GREEN)
        new_rect = rot_img.get_rect(center=old_center)
        new_mask = pg.mask.from_surface(rot_img)
        return rot_img, new_rect, new_mask

class Explotion(pg.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.all_sprites)
        self.images = game.explotion_img
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.game = game

        self.prev_frame_t = pg.time.get_ticks() / 1000
        self.frame = 0

    def update(self, *args):
        self.frame += self._frame_step(len(self.images))

        if self.frame == len(self.images) - 1:
            self.kill()

        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center = self.rect.center)

    def _frame_step(self, max):
        if pg.time.get_ticks() / 1000 - self.prev_frame_t > 0.1:
            self.prev_frame_t = pg.time.get_ticks() / 1000
            return 1
        else:
            return 0