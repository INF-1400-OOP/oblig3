import pygame as pg
from config import *

class Map:
    def __init__(self, map_file):
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

class Screen:
    def __init__(self, x, y, w, h):
        self.surf = pg.Surface((w, h), pg.SRCALPHA)
        self.rect = self.surf.get_rect(topleft=(x,y))
