import pygame as pg
from random import randint, uniform
from os import listdir
from os.path import join, dirname

from game_base_module import *
from config import *
from camera import Camera
from map import Map
from sprites import Player, Wall
from custom_events import *

vec = pg.math.Vector2

class Main(Loop):
    def __init__(self):
        # set path to main file
        self.path = dirname(__file__)
        
        # set path to directory containing spritesheets.
        # self.spritedir = join(self.path, "spritesheets")

        # super Loop object
        super().__init__(WIDTH, HEIGHT, FPS)

        # set center of screen
        self.center = vec(self.width // 2, self.height // 2)


        # self.controls = EventHandler(KEY_HELD_DOWN)
        # self.controls.handler = self.keypress
        # self.dispatcher.register_handler(self.controls)

    def load_data(self):
        self.textures = self.prep_images(listdir(join(self.path, "textures")))
        self.map = Map("testmap2.txt")

    def prep_images(self, imgnames:list[str]) -> dict:
        out_dict = {}
        for imgname in imgnames:
            out_dict[imgname.split(".")[0]] = pg.image.load(join(self.path, "textures", imgname))
        return out_dict

    def new(self):
        """ Called when game is initialized, can also be used for resetting the whole display. """
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()

        for row, tiles in enumerate(self.map.map):
            for column, tile in enumerate(tiles):
                if tile != "." and tile != "p":
                    Wall([self.all_walls, self.all_sprites], column, row, self.textures[tile])
                elif tile == "p":
                    self.player = Player(self, self.all_sprites, column, row, 10, 20, RED)

        self.camera = Camera(self.map.width, self.map.height)

    def update(self):
        # update all groups
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        # fill screen with background color
        self.screen.fill(BACKGROUND_COLOR)

        # Display FPS in caption
        pg.display.set_caption(f"{self.clock.get_fps():.2f}")
        
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()
    
if __name__ == "__main__":
    # call on simulation, execute new and run to start main loop
    mayhem_clone = Main()
    while True:
        mayhem_clone.new()
        mayhem_clone.run()
