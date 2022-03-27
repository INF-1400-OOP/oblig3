import pygame as pg
import numpy as np
from config import *
from game_base_module.settings import *
from smoke import SmokeParticle

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
        # self.image = pg.Surface((w,h), pg.SRCALPHA)
        self.image = texture
        self.texture = texture
        # self.image.blit(texture, (0,0))
        self.mask = pg.mask.from_surface(self.image)
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
        self.rot = 0
        self.landed = True
        self.thrust = False
        self.smoke = []

    def update(self, walls: pg.sprite.Group) -> None:
        self._check_landed()
        self.current_texture = self.textures[0]
        self.acc = vec(0, 0)
        img = self._select_texture()

        self._keymove()

        self.image, _, self.mask = self.rotate_img(img, self.rot)

        # If velocity is zero turn off gravity.

        if self.vel != vec(0, 0):
            self.acc += vec(0, 100) * 2

        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        
        self._impact(walls)

        # for particle in self.smoke:
        #     if not particle.alive:
        #         self.smoke.remove(particle)

        if len(self.smoke) > 20:
            last_particle = self.smoke[0]
            last_particle.kill()


    def _select_texture(self):
        if self.thrust:
            frame = int(self.game.t * 7) % (len(self.textures.keys()) - 1)
            return self.textures[frame + 1]
        else:
            return self.textures[0]

    def _check_landed(self):
        if self.vel != vec(0, 0):
            self.landed = False

    def _impact(self, walls: pg.sprite.Group):
        """ Check if self collide with blocks, if collision detected and it is not a landing pad, kill sprite."""

        collidewall = []

        for wall in walls:

            # Check if masks overlap. Add to list of walls which are collided with
            # The collide_mask function calculates a new mask for each time the function is called unless object has mask assigned to it.
            # Note that blocks dont need to update masks, however a sprite which rotates would have to update its mask to its rotation,
            # as the mask attribute is only a array of pixels which make a hitbox by differentiating transparent pixels from filled ones.

            if pg.sprite.collide_mask(self, wall):
                collidewall.append(wall)

        # Gather all walls texture id´s in a array
        ids = np.array([wall.texture_id for wall in collidewall])
        
        # Need to see if any of the blocks which have been collided with are either a "l" for landing platform or something else.
        # Because a mask or rect can collide with multiple blocks at once the program checks to see if any of the collided with blocks
        # are landing pads.

        if len(ids) > 0:
            if np.any(ids == "l"):

                # if speed in y direction is larger than 500 we kill the sprite.

                if self.vel[1] > 200:
                    self.kill()

                # Set velocity to the zero vector to "turn off" the gravity.

                self.vel = vec(0,0)
                self.rot = 0
                self.landed = True
            else:
                self.kill()

    def _keymove(self):
        key = pg.key.get_pressed()

        if key[pg.K_w]:
            self.acc -= (vec(0, 1) * SPRITE_SPEED).rotate(-self.rot)
            self.thrust = True
            smoke_pos = self.pos + vec(0, self.rect.height).rotate(-self.rot)
            self.smoke.append(SmokeParticle(self.game, smoke_pos, -self.vel*100))
        else:
            self.thrust = False
        if key[pg.K_a]:
            self.rot += 1
        if key[pg.K_d]:
            self.rot -= 1

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

class Wall(MayhemSprite):
    def __init__(self, 
            group: pg.sprite.Sprite, 
            x: int, 
            y: int, 
            texture: str,
            texture_id: str
            ):
        super().__init__(group, x, y, TILESIZE, TILESIZE, texture=texture)
        self.texture_id = texture_id
