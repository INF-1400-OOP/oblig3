import pygame as pg
vec = pg.math.Vector2

from game_base_module import randvec, GREEN
from config import *

class SmokeParticle(pg.sprite.Sprite):
    def __init__(self, game, pos, vel):
        super().__init__(game.all_sprites)
        self.game = game
        self.d_scale_factor = 0.1
        self.image = self.scale(game.smoke_img, self.d_scale_factor)
        self.rect = self.image.get_rect(center=pos)
        self.alpha = 128
        self.d_alpha = 6
        self.vel = vel * 400
        self.pos = pos

    def update(self, *args):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        self.d_scale_factor += 0.005
        self.alpha -= self.d_alpha

        if self.alpha < 0:
            self.alive = False
            self.game.all_sprites.remove(self)

        self.d_alpha -= 0.1

        if self.d_alpha < 1.5:
            self.d_alpha = 1.5

        self.image = self.scale(self.game.smoke_img, self.d_scale_factor)
        self.image.set_alpha(self.alpha)

    @staticmethod
    def scale(img, factor):
        size = vec(img.get_size()) * factor
        scaled_image = pg.transform.scale(img, (int(size[0]), int(size[1])))
        return scaled_image

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


