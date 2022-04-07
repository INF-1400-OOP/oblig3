""" This module contains the Player class which is the main character of the game implementation. """

from sprites import *
from effects import SmokeParticle, Explotion, LaserBeam
from controller import Controller

class Player(MayhemSprite):
    """ Player sprite. The player is the main sprite which has registered controls, animations, a score and the ability to take out other players. Has parent class MayhemSprite.
    
    Attributes
    ----------
    textures : dict
        Dictionary containing textures for sprite.
    game : object
        Main game object.
    screen : pygame.Surface
        Screen object dedicated to tracking this sprite.
    fuel : FuelTank
        FuelTank object for this sprite which keeps track of fuel level, and blitting status to the screen.
    controller : Controller
        A object for registering methods for different types of movement.
    player_n : int
        Player number. Either 1 for player 1 or 2 for player 2.
    pos, vel, acc, rot: pygame.Vector2, pygame.Vector2, pygame.Vector2, int
        Attributes which keep track of the spatial parameters.
    landed : bool
        Attribute to keep track of if the spacecraft has landed. (default True)
    thrust: bool
        Attribute to keep track of if the spacecraft is applying thrust. (default False)
    prev_shot : bool
        Attribute to keep track of the previous time when the spacecraft shot it's laser gun. (defaul 0)
    exploded : bool
        Attribute to keep track of if the spacecraft has exploded. (defaul False)

    Methods
    -------
    update(walls)
        updates object once per frame
    up()
        method for what happens when a up key is pressed.
    down()
        method for what happens when a down key is pressed.
    left()
        method for what happens when a left key is pressed.
    right()
        method for what happens when a right key is pressed.
    kill(reason)
        method that when called removes sprite from any groups. Also this method has been extended to command game object to respawn a new player object.
    rotate_img(img, angle)
        Rotates image by given angle.
    """
    def __init__(
            self, 
            game: object,
            controls: Controller,
            x: int, 
            y: int, 
            textures: dict,
            player_n: int,
            screen: pg.Surface
            ):
        """
        Args
        ----
        game: Main
            Main game object.
        controls: Controller
            A object for registering methods for different types of movement.
        x, y: int
            Starting positions of player object.
        textures: dict
            A dictionary with different textures that look like a spaceship.
        player_n: int
            A integer keeping track if object is player 1 or player 2.
        screen: pygame.Surface
            The screen which is dedicated to following this player.
        """

        self.textures = textures

        # Set current texture to the static spaceship graphic.
        self.current_texture = textures[0]
        w, h = self.current_texture.get_rect().size

        # super the MayhemSprite class.
        super().__init__([game.all_sprites, game.all_players], x, y, w, h, texture=self.current_texture)

        # Keep track of game, dedicated screen, fuel, and controller
        self.game = game
        self.screen = screen
        self.fuel = FuelTank(self)
        self.controller = controls
        self.player_n = player_n

        # Positional attributes.
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0

        # Other attributes.
        self.landed = True
        self.thrust = False
        self.prev_shot = 0
        self._configure_controls()
        self.exploded = False

    def update(self, walls: pg.sprite.Group) -> None:
        """ Generic pygame sprite required update method for updating sprite on a per frame basis.
        
        Args:
            walls: pygame.sprite.Group
                Game spritegroup containing all walls used in active instance of game.
        """

        # Set thrust to False every frame and reset acceleration.
        self.thrust = False
        self.acc = vec(0, 0)

        # Force controller to register our keystrokes with predefined methods for the different possible movement vectors.
        self.controller.register_keystrokes()

        # Check if landed and if hit by projectile and also select what texture to blit.
        self._check_landed()
        self._hit_by_projectile()
        self._apply_gravity()
        img = self._select_texture()

        # Set the image, and mask to the output of rotate_img method.
        self.image, _, self.mask = self.rotate_img(img, self.rot)

        # Use Euler-cromer differential equation solver for estimating a solution for position relative to velocity and acceleration vector.

        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        
        # Check for impacts with walls, if player should explode and if player should refuel.

        self._impact(walls)
        self._if_explode()
        self._refuel()

    def _apply_gravity(self) -> None:
        """ Method for applying gravity. """
        
        # As we do not want the player to slowly fall throught the floor we only apply gravity when player is not landed and thus is airborne.

        if not self.landed:
            self.acc += vec(0, 1) * GRAVITY_MAG

    def _select_texture(self) -> pg.Surface:
        """ Method for animating sprite. 
        
        Returns:
            texture: pygame.Surface
                current texture to be displayed on main player surface.
        """

        # If thrust is not active then we use the static image with position 0 in texture dict which is just the image for when static.

        texture = self.textures[0]

        # When thrust is active animate

        if self.thrust:
            frame = int(self.game.t * 7) % (len(self.textures.keys()) - 1)

            # as texture with zero index is the static image we only iterate over frame + 1 to last frame in texture dictionary.
            
            texture = self.textures[frame + 1]

        return texture

    def _check_landed(self) -> None:
        """ Method for keeping track of the landed attribute. If velocity not zero vector; set landed to False. """
        if self.vel != vec(0, 0):
            self.landed = False

    def _impact(self, walls: pg.sprite.Group) -> None:
        """ Check if self collide with blocks, if collision detected and it is not a landing pad, kill sprite.
        
        Args:
            walls: pygame.sprite.Group
                Group object containing all walls.
        """

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
                    self.kill(reason="wall")

                # Set velocity to the zero vector to "turn off" the gravity.

                self.vel = vec(0,0)
                self.rot = 0
                self.landed = True
            else:
                self.kill(reason="wall")

    def up(self) -> None:
        """ Method for moving up. This method does a couple of important things:
        
        1. Check that fuel tank is not empty
        2. Apply a acceleration to the heading of the spacecraft.
        3. Set thrust attribute to True.
        4. Call on method _exhaust, which creates the SmokeParticle objects.
        5. Call on method _use_fuel, which drains the fuel tank.
        """

        # Check if there is fuel left, if not, then do not execute the code below.
        if self.fuel.amount == 0:
            return

        # If up key is pressed, set thrust to true and increase the acceleration vector and apply rotation.

        self.acc -= (vec(0, 1) * SPRITE_FORCE).rotate(-self.rot)
        self.thrust = True

        self._exhaust()

        self._use_fuel()
    
    def left(self) -> None:
        self.rot += 2
    
    def right(self) -> None:
        self.rot -= 2

    def down(self) -> None:
        self._shoot()

    def _configure_controls(self) -> None:

        # Configure given controller methods as the predefined local methods for moving up, left, right and down.

        self.controller.set_key_bindings(
            up=self.up,
            left=self.left,
            right=self.right,
            down=self.down
        )

    def _exhaust(self) -> None:
        """ Method for creating smoke when thrust is active by instantiating the SmokeParticle class. """

        # Calculate the starting posistion of the smoke as the bottom of the sprite plus some margin, then rotated by the rotation of the sprite.

        smoke_pos = self.pos + vec(0, self.rect.height * 0.75).rotate(-self.rot)

        # Calculate smoke starting velocity as the negative rotation and make it as a vector for the SmokeParticle vel parameter.

        smoke_vel = vec(0,1).rotate(-self.rot)

        # Create a new smoke sprite object.

        SmokeParticle(self.game, smoke_pos, smoke_vel)

    def _shoot(self) -> None:
        """ Method for shooting. Instantiates a LaserBeam object. """

        # Check if time from previous shot is less than SPRITE_LOAD_DURATION, if yes; instantiate LaserBeam object and reset time of last shot.

        if pg.time.get_ticks() / 1000 - self.prev_shot > SPRITE_LOAD_DURATION:
            LaserBeam(self, self.game, self.pos - vec(0, self.rect.height / 2).rotate(-self.rot), -self.rot)
            self.prev_shot = pg.time.get_ticks() / 1000

    def _if_explode(self) -> None:
        """ Method for checking if player has been killed and if yes then make a explotion object. """

        # If player is not alive and has not already exploded, then instantiate a Explotion object.
        if not self.alive() and not self.exploded:
            Explotion(self.game, self.pos)

    def _hit_by_projectile(self) -> None:
        """ Method for checking if player collide with any laser. """

        # Get list of collided lasers.

        laser = pg.sprite.spritecollideany(self, self.game.all_projectiles)

        # If no collision detected spritecollideany returns None, threfore early exit if no laser collision.

        if laser is None:
            return

        # Each laser object has a sender attribute to check that we dont register collisions between laser and player when player shoots and rectangles probably overlap in some rotations.
        
        if laser.sender != self:
                self.kill(reason="shot")

    def _get_reset_point(self) -> pg.Rect:
        """ Method for finding a respawn point - the landing pad the furthest away from the opponent.
        
        Returns:
            pg.Rect
                Landing pad furthest away from opponent.
        """
        
        opponent = None

        # Iterate through registered players in game

        for player in self.game.all_players:

            # set opponent to player if not self.

            if player != self:
                opponent = player

        
        furthest_lp = None
        dist = 0
        
        # Iterate over all wall sprites and look for the ones with texture id as "l" for landing pad.

        for wall in self.game.all_walls:
            if wall.texture_id == "l":

                # Find the distance between opponent and each candidate landing pad.

                calc_dist = vec(wall.rect.center).distance_to(vec(opponent.rect.center))
                
                # Choose closest one.

                if calc_dist > dist:
                    furthest_lp = wall
                    dist = calc_dist

        return furthest_lp.rect

    def kill(self, reason: str) -> None:
        """ Modify the standard kill method of sprites to also run a code block in game which respawns a new player. 
        
        Args
        ----
        reason : str
            Why was the player killed, either 'shot' or 'wall'.
        """
      
        super().kill()
        self.game.respawn(self.player_n, self._get_reset_point(), reason)

    def _use_fuel(self) -> None:
        """ When thrusting we subtract one fuel entity. """
        self.fuel.amount -= 1

    def _refuel(self) -> None:
        """ Method for refueling when landed. """

        # check both if landed and that fuel amount dont exceed a full tank.
        if self.landed and self.fuel.amount <= self.fuel.max_amount:
            self.fuel.amount += 2

    @staticmethod
    def rotate_img(img: pg.Surface, angle: int) -> tuple[pg.Surface, pg.Rect, pg.mask.Mask]:
        """ Rotates image by given angle. 
        
        Args
        ----
        img: pygame.Surface
            Original image.
        angle: float
            Angle to be rotated by

        Returns
        -------
        rot_img : pygame.Surface
            New rotated image.
        new_rect : pygame.Rect
            new rotated (and scaled) rect.
        new_mask : pygame.mask.Mask
        """

        old_center = img.get_rect().center
        rot_img = pg.transform.rotate(img, angle)
        rot_img.set_colorkey(GREEN)
        new_rect = rot_img.get_rect(center=old_center)
        new_mask = pg.mask.from_surface(rot_img)
        return rot_img, new_rect, new_mask
