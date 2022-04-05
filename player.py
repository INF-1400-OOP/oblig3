from sprites import *
from effects import SmokeParticle, Explotion, LaserBeam

class Player(MayhemSprite):
    def __init__(
            self, 
            game: object,
            controls: object,
            x: int, 
            y: int, 
            textures: dict,
            player_n: int,
            screen: pg.Surface
            ):
        self.textures = textures
        self.current_texture = textures[0]
        w, h = self.current_texture.get_rect().size
        super().__init__([game.all_sprites, game.all_players], x, y, w, h, texture=self.current_texture)
        self.game = game
        self.screen = screen
        self.fuel = FuelTank(self)
        self.controller = controls
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0
        self.landed = True
        self.thrust = False
        self.smoke = []
        self.prev_shot = 0
        self._configure_controls()
        self.exploded = False
        self.player_n = player_n

    def update(self, walls: pg.sprite.Group) -> None:
        self.thrust = False
        self.acc = vec(0, 0)
        self.controller.register_keystrokes()
        self._check_landed()
        self._hit_by_projectile()
        img = self._select_texture()

        self.image, _, self.mask = self.rotate_img(img, self.rot)

        self._apply_gravity()

        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        
        self._impact(walls)
        self._if_explode()
        self._refuel()

    def _apply_gravity(self):
        if not self.landed:
            self.acc += vec(0, 200)

    def _select_texture(self):
        texture = self.textures[0]
        if self.thrust:
            frame = int(self.game.t * 7) % (len(self.textures.keys()) - 1)
            texture = self.textures[frame + 1]
        return texture

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

    def up(self):

        # Check if there is fuel left, if not, then do not execute the code below.
        if self.fuel.amount == 0:
            return

        # If up key is pressed, set thrust to true and increase the acceleration vector and apply rotation.

        self.acc -= (vec(0, 1) * SPRITE_SPEED).rotate(-self.rot)
        self.thrust = True

        self._exhaust()

        self._use_fuel()
    
    def left(self):
        self.rot += 1
    
    def right(self):
        self.rot -= 1

    def down(self):
        self._shoot()

    def _configure_controls(self):
        self.controller.set_key_bindings(
            up=self.up,
            left=self.left,
            right=self.right,
            down=self.down
        )

    def _exhaust(self):
        # Calculate the starting posistion of the smoke as the bottom of the sprite plus some margin, then rotated by the rotation of the sprite.

        smoke_pos = self.pos + vec(0, self.rect.height * 0.75).rotate(-self.rot)

        # Create a new smoke sprite and add it to the smoke list.

        self.smoke.append(SmokeParticle(self.game, smoke_pos, vec(0,1).rotate(-self.rot)))

    def _shoot(self):
        if pg.time.get_ticks() / 1000 - self.prev_shot > 0.2:
            LaserBeam(self, self.game, self.pos - vec(0, self.rect.height / 2).rotate(-self.rot), -self.rot)
            self.prev_shot = pg.time.get_ticks() / 1000

    def _if_explode(self):
        if not self.alive() and not self.exploded:
            Explotion(self.game, self.pos)

    def _hit_by_projectile(self):
        laser = pg.sprite.spritecollideany(self, self.game.all_projectiles)

        if laser is None:
            return

        if laser.sender != self:
                self.kill()

    def _get_reset_point(self):
        opponent = None
        for player in self.game.all_players:
            if player != self:
                opponent = player
        furthest_lp = None
        dist = 0
        for wall in self.game.all_walls:
            if wall.texture_id == "l":
                calc_dist = vec(wall.rect.center).distance_to(vec(opponent.rect.center))
                if calc_dist > dist:
                    furthest_lp = wall
                    dist = calc_dist
        return furthest_lp.rect

    def kill(self):
        super().kill()
        self.game.respawn(self.player_n, self._get_reset_point())

    def _use_fuel(self):
        self.fuel.amount -= 1

    def _refuel(self):
        if self.landed and self.fuel.amount <= self.fuel.max_amount:
            self.fuel.amount += 2

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
