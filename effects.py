""" Module containing all visual effects which does not interact with any other sprites but are there only for the visuals (Except for LaserBeam but you get the point). """

import pygame as pg
vec = pg.math.Vector2

from game_base_module import randvec, GREEN
from config import *

class SmokeParticle(pg.sprite.Sprite):
    """ SmokeParticle class which inherits from pygame.sprite.Sprite. When multiple SmokeParticles are created in succession it appears as a cloud of smoke or exhaust.
    
    Note this class is GREATLY inspired by the code found in https://github.com/tank-king/Tutorials/tree/main/Python%20Pygame/smoke_effect.

    Attributes
    ----------
    game : object
        Main game object.
    d_scale_factor : float
        A factor to scale the image with. factor < 1 means image is scaled down, likewise factor > 1 means image is enlarged.
    image : pygame.Surface
        Image to be blitted to screen.
    rect : pygame.Rect
        Rectangle of image.
    alpha : float
        Transparency pixel value of image, 0 <= alpha <= 255. (default 128).
    d_alpha : float
        Rate of change in alpha. Think of it like the discrete time derivative of the alpha as this value is subtracted each iteration. (default 6)
    vel : pygame.math.Vector2
        Velocity of smoke particle.
    pos : pygame.math.Vector2
        Position of smoke particle.

    Methods
    -------
    update(*args)
        Update position, velocity, transparency and scale of image per frame. Also checks if smoke particle can be removed.
    scale(img, factor)
        Scales the given image by given factor then returns scaled surface image.
    """
    def __init__(self, game:object, pos:vec, vel:vec):
        """
        Args
        ----
        game : object
            Main game object.
        pos : pygame.math.Vector2
            Starting position of SmokeParticle.
        vel : pygame.math.Vector2
            Starting velocity of SmokeParticle.
        """
        super().__init__(game.all_sprites)
        self.game = game
        self.d_scale_factor = 0.1
        
        # Starting image is large, therefore we already scale it down to d_scale_factor.
        self.image = self.scale(game.smoke_img, self.d_scale_factor)
        self.rect = self.image.get_rect(center=pos)

        self.alpha = 128
        self.d_alpha = 6
        self.vel = vel * 400
        self.pos = pos

    def update(self, *args):
        """ Update position, velocity, transparency and scale of image per frame. Also checks if smoke particle can be removed.
        
        Args
        ----
        *args : any
            -
        """

        # Using Euler cromer method to update position based on velocity
        self.pos += self.vel * self.game.dt

        # Set rectangle position to pos vector.
        self.rect.center = self.pos

        # change in d_scale_factor. Sort of like a derivative of the scale factor at 0.005. Therefore image is enlarged by this factor each frame.
        self.d_scale_factor += 0.005

        # update alpha based on change in alpha. (apply derivative)
        self.alpha -= self.d_alpha

        # Kill sprite if completely invisible.
        if self.alpha < 0:
            self.alive = False
            self.game.all_sprites.remove(self)

        # Change the change in alpha by this factor. Therefore here we apply a sort of second derivative to the change in alpha.
        self.d_alpha -= 0.1

        # Set change in alpha to constant if value is too small.
        if self.d_alpha < 1.5:
            self.d_alpha = 1.5
        
        # Scale and set alpha of image.
        self.image = self.scale(self.game.smoke_img, self.d_scale_factor)
        self.image.set_alpha(self.alpha)

    @staticmethod
    def scale(img: pg.Surface, factor:float) -> pg.Surface:
        """ Scales the given image by given factor then returns scaled surface image. 
        
        Args
        ----
        img : pygame.Surface
            Image to be scaled.
        factor : float
            Factor to scale image by.
        
        Returns
        -------
        scaled_image : pygame.Surface
            The scaled image.
        """

        # Get the size of given image and caluclate new size.
        size = vec(img.get_size()) * factor

        # scale image by the closest integers to the calculated size.
        scaled_image = pg.transform.scale(img, (int(size[0]), int(size[1])))
        return scaled_image

class Explotion(pg.sprite.Sprite):
    """ Explotion class which inherits from pygame.sprite.Sprite. Shows an explotion for a couple of frames, then vanishes.
    
    Attributes
    ----------
    images : list[pygame.Surface]
        List containing the surfaces which are used in the animation.
    image : pygame.Surface
        The image displayed.
    rect : pygame.Rect
        Rectangle of image
    game : object
        Main game object
    prev_frame_t : float
        Time of previous frame start.
    frame : int
        Current frame. (default 0).
    
    Methods
    -------
    update(*args)
        Method for updating each image to use in animation. Also kills sprite and removes object from all sprite groups.
    _frame_step()
        Method that changes the frame if a certain amount of time has passed (0.1s). Therefore the explotion lasts for a total of 0.1 * len(images) seconds.
    """
    def __init__(self, game:object, pos:vec):
        """
        Args
        ----
        game : object
            Main game object.
        pos : pygame.math.Vector2
            The position where the explotion is to take place.
        """
        super().__init__(game.all_sprites)
        self.images = game.explotion_img

        # initially use first image.
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.game = game

        # find starting time of explotion.
        self.prev_frame_t = pg.time.get_ticks() / 1000

        # set current frame to 0.
        self.frame = 0

    def update(self, *args:any):
        """ Method for updating each image to use in animation. Also kills sprite and removes object from all sprite groups. 
        
        Args:
            *args : any
                -
        """

        # increase frame by output of _frame_step.
        self.frame += self._frame_step()

        # kill explotion if frame is the last frame.
        if self.frame == len(self.images) - 1:
            self.kill()

        # set image to correct frame.
        self.image = self.images[self.frame]

        # recenter image
        self.rect = self.image.get_rect(center = self.rect.center)

    def _frame_step(self):
        """ Method that changes the frame if a certain amount of time has passed (0.1s). Therefore the explotion lasts for a total of 0.1 * len(images) seconds. """

        # Calculate time between frames. If time exceeds 0.1 s, change frame.
        if pg.time.get_ticks() / 1000 - self.prev_frame_t > 0.1:
            self.prev_frame_t = pg.time.get_ticks() / 1000
            return 1

        return 0

class LaserBeam(pg.sprite.Sprite):
    """ Class LaserBeam which inherits from pygame.sprite.Sprite. A laser shot from the top of a spacecraft. If collision with wall - kill laser,
    if collision with player, kill player. 
    
    Attributes
    ----------
    game : object
        Main game object.
    sender : Player
        The sender of the laser beam. Used to not collide with the one who shot the laser.
    pos : pygame.math.Vector2
        The position of the LaserBeam
    dir : int
        The direction the LaserBeam is traveling.
    image : pygame.Surface
        Image to display on the screen.
    rect : pygame.Rect
        Rectangle of image.
    mask : pygame.mask.Mask
        Mask of image.
    vel : pygame.math.Vector2
        Velocity of object.

    Methods
    -------
    update(*args)
        update position and check for collisions.
    _collide()
        check for collision with walls.
    rotate_img(img, angle)
        Method to rotate the image given a image and an angle.
    """
    def __init__(self,
            sender:object,
            game:object,
            pos: vec,
            direction: int
            ):
        """
        Args
        ----
        sender : Player
            The sender of the laser beam. Used to not collide with the one who shot the laser.
        game : object
            Main game object.
        pos : pygame.math.Vector2
            The starting position of the LaserBeam
        direction : int
            The starting direction the LaserBeam is traveling.
        """
        
        self.game = game
        self.sender = sender
        super().__init__(game.all_sprites, game.all_projectiles)
        self.pos = pos
        self.dir = direction
        self.image = self.game.laser_img
        
        # Set correct rotation of image rect and mask as well as velocity.
        self.image, self.rect, self.mask = self.rotate_img(self.image, -self.dir)
        self.vel = vec(0, -PROJECTILE_SPEED).rotate(self.dir)

    def update(self, *args):
        """ update position and check for collisions.
        Args
        ----
        *args : any
            -
        """
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self._collide()

    def _collide(self):
        """ Method to rotate the image given a image and an angle. """
        for wall in self.game.all_walls:

            # check if masks overlap.
            if pg.sprite.collide_mask(self, wall):
                self.kill()

    @staticmethod
    def rotate_img(img:pg.Surface, angle:int) -> tuple[pg.Surface, pg.Rect, pg.mask.Mask]:
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


