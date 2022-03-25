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
        self.col = col
        self.texture = texture
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
            col: tuple[int, int, int],
            textures: dict
            ):
        self.textures = textures
        self.current_texture = textures[0]
        w, h = self.current_texture.get_rect().size
        super().__init__(groups, x, y, w, h, texture=self.current_texture)
        self.game = game
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.controls = None
        self.is_stationary = False

    def update(self, walls):
        if self.vel == vec(0,0):
            self.is_stationary = True
        else:
            self.is_stationary = False

        self.acc = vec(0, 0)
        self._keymove()

        if not self.is_stationary:
            self.acc += vec(0, 100) * 2

        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        
        self._impact(walls)


    def _impact(self, walls):
        collidewall = pg.sprite.spritecollide(self, walls, False)

        for wall in collidewall:
            if wall.texture == self.game.textures["l"]:
                if self.vel != vec(0, 0):
                    if self.vel.normalize()[1] > 0 and self.vel[1] > 200:
                        self.kill()
                self.vel = vec(0, 0)

            else:
                self.kill()

    def _keymove(self):
        key = pg.key.get_pressed()

        if key[pg.K_w]:
            self.acc[1] -= 1000
            self.current_texture = self.textures[1 + (int(self.game.t) % (len(self.textures) - 1))]
        if key[pg.K_s]:
            self.acc[1] += 300
        if key[pg.K_a]:
            self.acc[0] -= 300
        if key[pg.K_d]:
            self.acc[0] += 300

class Wall(MayhemSprite):
    def __init__(self, 
            group: pg.sprite.Sprite, 
            x: int, 
            y: int, 
            texture: str
            ):
        super().__init__(group, x, y, TILESIZE, TILESIZE, texture=texture)