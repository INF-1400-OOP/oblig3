""" This module contains the Map and Screen class. Use the Screen class for a object like one of the screens in a split-screen implementation. The Map class
is used to easily read a text file and converting it to a Map object usable for easy map-generation in a game.
"""

import pygame as pg
from config import *

class Map:
    """ Map object used for reading a text file containing symbols representing a tile.

    Note: This class is greatly inspired by the implementation at: https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2004/tilemap.py
    
    Attributes
    ----------
    _f : str
        Path to map text file.
    map : list
        Each entry is a string containing symbols representing a tile.
    mapwidth : int
        Number of symbols in each string. Represents lenght of rows.
    mapheight : int
        Number of rows in map.
    width : int
        mapwidth multiplied by the TILESIZE.
    height : int
        mapheight multiplied by the TILESIZE.
    
    Methods
    -------
    load_map()
        returns the read text file into a list of strings.
    """
    def __init__(self, map_file):
        """
        Args
        ----
        map_file : str
            Path to map text file.
        """
        self._f = map_file
        self.map = self.load_map()
        self.mapwidth = len(self.map[0])
        self.mapheight = len(self.map)
        self.width = self.mapwidth * TILESIZE
        self.height = self.mapheight * TILESIZE

    def load_map(self):
        objects = []
        with open(self._f, "r") as f:
            for row in f:
               objects.append(row.strip())
        return objects

class Camera:
    """ Camera object assigned to a sprite to follow which is the target in update() function. This implementation also does not move camera rectangle outside of boundaries.
    
    Works by moving all sprites in the opposite direction of the main player sprite. Therefore use apply on all sprites, and use update on main sprite to follow.
    
    Note: This class is greatly inspired by the implementation at: https://github.com/kidscancode/pygame_tutorials/blob/master/tilemap/part%2004/tilemap.py

    Attributes
    ----------
    camera : pygame.Rect
        Rectangle where everything is to be drawn inside.
    width : int
        Width of camera rectangle.
    height : int
        Height of camera rectangle.
    
    Methods
    -------
    apply(rect)
        Apply movement to given rect. Move rect inside cameras rectangle.
    update(target)
        Follows target by moving sprites relative to this as it sets the cameras rectangle to a new position based on the given target. This method also takes the
        boundaries into account by not moving the camera rectangle outside of the given edges.
    """
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect:pg.Rect) -> pg.Rect:
        """ Apply movement to given rect. Move rect inside cameras rectangle.
        
        Args
        ----
        rect : pygame.Rect
            Rect of sprites to move inside camera rect.

        Returns
        -------
        rect : pygame.Rect
            Moved rectangle of given rect.
        """
        return rect.move(self.camera.topleft)

    def update(self, target:pg.sprite.Sprite) -> None:
        """ Follows target by moving sprites relative to this as it sets the cameras rectangle to a new position based on the given target. This method also takes the
        boundaries into account by not moving the camera rectangle outside of the given edges.
        
        Args
        ----
        target : pygame.sprite.Sprite
            Sprite that camera will follow.
        """
        x = -target.rect.x + WIDTH // 4
        y = -target.rect.y + HEIGHT // 2

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH // 2), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height)

class Screen:
    """ Screen object for blitting to. Works nicely for passing to a sprite object, for a dedicated screen per player sprite. 
    
    Attributes
    ----------
    surf : pygame.Surface
        The surface of the screen.
    rect : pygame.Rect
        The rectangle of the surface.
    """
    def __init__(self, x, y, w, h):
        """
        Args
        ----
        x : int
            x position.
        y : int
            y position.
        w : int
            Width.
        h : int 
            Height.
        """
        self.surf = pg.Surface((w, h), pg.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x,y))
