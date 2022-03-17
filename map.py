import pygame as pg

class Map:
    def __init__(self, map_file):
        self._f = map_file
        self.map = self.load_map()

    def load_map(self):
        objects = []
        with open(self._f, "r") as f:
            for row in f:
               objects.append(row.strip())
        return objects

