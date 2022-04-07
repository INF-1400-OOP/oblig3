""" Module containing Base class MayhemSprite and child class Wall. Also has FuelTank and Scoreboard sprites. Generally things which are drawn to the
screen are contained here with some exceptions. """

import pygame as pg
import numpy as np
from config import *
from game_base_module.settings import *
from game_base_module import map_val, draw_text

vec = pg.math.Vector2

class MayhemSprite(pg.sprite.Sprite):
    """ MayhemSprite base class. Gives some general attributes and instantiates pygame.sprite.Sprite.
    
    Attributes
    ----------
    image : pygame.Surface
        Image to be blitted
    texture : pygame.Surface
        Keeps track of what image is used.
    mask : pygame.mask.Mask
        Mask of object used for collision detection.
    rect : pygame.Rect
        Rectangle of image.
    x, y : int, int
        Positions of object.
    """
    def __init__(
            self,
            groups: pg.sprite.Group,
            x: int,
            y: int,
            w: int,
            h: int,
            texture=None
            ):
        """
        Args
        ----
        groups : pygame.sprite.Group
            Groups which object will be added to.
        x, y, w, h : int, int, int, int
            Dimensions of object.
        texture : pygame.Surface|None
            Texture and image of sprite. (Default None)
        """

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
    """ Wall child class of MayhemSprite. Used to place a wall in the game from the map.
    
    Attributes
    ----------
    image : pygame.Surface
        Image to be blitted
    texture : pygame.Surface
        Keeps track of what image is used.
    mask : pygame.mask.Mask
        Mask of object used for collision detection.
    rect : pygame.Rect
        Rectangle of image.
    x, y : int, int
        Positions of object.
    texture_id : str
        String representing what symbol was read from the map text file.
    """
    def __init__(self,
            group: pg.sprite.Sprite,
            x: int,
            y: int,
            texture: str,
            texture_id: str,
            ):
        """
        Args
        ----
        group : pygame.sprite.Sprite
            Groups which object will be added to.
        x, y : int, int
            Position of object.
        texture : pygame.Surface
            Texture and image of sprite.
        texture_id : str
            String representing what symbol was read from the map text file.
        """

        super().__init__(group, x, y, TILESIZE, TILESIZE, texture=texture)
        self.texture_id = texture_id

class FuelTank(pg.sprite.Sprite):
    """ Fuel tank object attached to a Player object. Child class of pygame.sprite.Sprite.
    
    Attributes
    ----------
    image : pygame.Surface
        Surface image blitted to the screen. This surface is a red box.
    rect : pygame.Rect
        Rectangle of image.
    amount_surf: pygame.Surface
        The overlayed surface of the image surface which is a green box and will shrink in size as fuel is used.
    amount_rect : pygame.Rect
        The rect of amount_surf
    max_amount : int
        The maximum amount of fuel there is room for in the FuelTank. (default 2000)
    amount : int
        The current amount of fuel in the FuelTank. (default 2000)
    
    Methods
    -------
    update()
        Updates the size of the overlayed amount_surf surface to reflect the amount of fuel left in the tank.
    draw(surf)
        Blits image to surf (main surface).
    """
    def __init__(self, player):
        super().__init__(player.game.all_statuses)
        w, h = 100, 20
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=vec(player.screen.rect.topleft) + vec(100, 40))
        self.image.fill(RED)
        self.amount_surf = pg.Surface((w, h), pg.SRCALPHA)
        self.amount_rect = self.amount_surf.get_rect(topleft=self.rect.topleft)
        self.amount_surf.fill(GREEN)
        self.max_amount = 2000
        self.amount = self.max_amount

    def update(self):
        """ Updates the size of the overlayed amount_surf surface to reflect the amount of fuel left in the tank. """

        # Fill image with red color.
        self.image.fill(RED)

        # update size of surface if amount is larger than 0.
        if self.amount >= 0:

            # adjust size using game_base_modue.util's map_val function.
            self.amount_rect.width = map_val(self.amount, 0, self.max_amount, 0, self.rect.width)

            # transform the scale of the amount_surface to the new width.
            self.amount_surf = pg.transform.scale(self.amount_surf, self.amount_rect.size)

        # blit amount_surf to main image surface.
        self.image.blit(self.amount_surf, (0, 0))

    def draw(self, surf):
        """ Blits image to surf (main surface). """

        surf.blit(self.image, self.rect.topleft)

class Scoreboard(pg.sprite.Sprite):
    """ Scoreboard class, child of pygame.sprite.Sprite. Used for keeping track of the score of each player.
    
    Attributes
    ----------
    image : pygame.Surface
        Surface to be shown.
    rect : pygame.Rect
        Rectangle of image.
    _scores : dict
        Keeps track of scores.
    _prev_scores : dict
        Keeps track of previous score.
    
    Methods
    -------
    update()
        Update what to be shown in the scores.
    draw(surf)
        Draw image to surf which is main screen.
    @property(scores)
        A Getter of scores.
    give_point(player_n)
        Give a point to player number player_n
    reset_score()
        Set all scores to zero.
    __str__()
        Prettier printing.
    """
    def __init__(self, game):
        """
        Args
        ----
        game : object
            Main loop.
        """
        super().__init__(game.all_statuses)
        self.image = pg.Surface((100, 100), pg.SRCALPHA)
        self.rect = self.image.get_rect(midtop=game.center + vec(0, -game.height // 2))
        self._scores = {"1": 0, "2": 0}
        self._prev_scores = self._scores
        self.game = game

    def update(self):
        """ Update what to be shown in the scores. """

        #self.image.fill(WHITE)

        # # if there has not been any changes to the scores quit function early
        # if self._prev_scores == self._scores:
        #     return
        # draw_text(self.game.screen, f"Player 1 : {self._scores['1']}", 28, self.rect.x, self.rect.y+20, BLACK, center=False)
        pass

    def draw(self, surf):
        """ Draw image to surf which is main screen. """

        # surf.blit(self.image, self.rect.center)
        pass

    @property
    def scores(self):
        """ A Getter of scores. """

        return self._scores

    def give_point(self, player_n):
        """ Give a point to player number player_n """

        self._scores[player_n] += 1

    def reset_score(self):
        """ Set all scores to zero. """

        self._scores["1"] = 0
        self._scores["2"] = 0

    def __str__(self):
        """ Prettier printing. """

        return f"p1: {self._scores['1']}\np2: {self._scores['2']}"
