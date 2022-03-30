import pygame as pg
vec = pg.math.Vector2

from game_base_module import randvec

class SmokeParticle(pg.sprite.Sprite):
    def __init__(self, game, pos, vel):
        super().__init__(game.all_sprites)
        self.game = game
        self.alive = True
        self.d_scale_factor = 0.1
        self.image = self.scale(game.smoke_img, self.d_scale_factor)
        self.rect = self.image.get_rect(center=pos)
        self.alpha = 255
        self.d_alpha = 4
        self.vel = vel
        self.pos = pos
        
    def update(self, *args):
        self.vel -= randvec(0.01, 0.05, 0.01, 0.05) * self.game.dt
        self.pos += self.vel * self.game.dt

        self.d_scale_factor += 0.005
        self.alpha -= self.d_alpha

        if self.alpha < 0:
            self.alpha = 0
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