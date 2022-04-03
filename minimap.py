import pygame as pg
import numpy as np
from config import HEIGHT, WIDTH
from game_base_module import map_val

vec = pg.math.Vector2

class Minimap(pg.sprite.Sprite):
    def __init__(self, game, screen, map):
        super().__init__(game.minimaps)
        self.image = pg.Surface((game.width // 6, game.height // 6), pg.SRCALPHA)
        self.rect = self.image.get_rect(midtop=(game.width // 2, 0))
        self.map = map

    def update(self):
        self.surf_pix = pg.PixelArray(self.image)
        
        map_array = np.zeros(self.surf_pix.shape[:2])
        for i, row in enumerate(self.map):
            for j, col in enumerate(row):
                if self.map[i][j] != "." and self.map[i][j] != "1" and self.map[i][j] != "2":
                    map_array[i, j] = 9
                elif self.map[i][j] == "1":
                    map_array[i, j] = 1
                elif self.map[i][j] == "2":
                    map_array[i, j] = 2

        self.surf_pix[True] = pg.Color("black")

        self.surf_pix[map_array == 9] = pg.Color("gray")

        self.surf_pix[map_array == 1] = pg.Color("red")
        self.surf_pix[map_array == 2] = pg.Color("green")

        self.image = self.surf_pix.make_surface()
