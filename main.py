import pygame as pg
from os import listdir
from os.path import join, dirname

from game_base_module import *
from config import *
from camera import Camera
from map import Map
from sprites import Wall
from custom_events import *
from player import Player
from controller import Controller

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

        self.resethandler = EventHandler(pg.KEYDOWN)
        self.resethandler.handler = self.reset
        self.dispatcher.register_handler(self.resethandler)

    def load_data(self):
        self.map = Map("testmap1.txt")
        self.textures = self.prep_images(join(self.path, "textures"), listdir(join(self.path, "textures")))
        self.rocket_textures = self.prep_images(join(self.path, "spritesheets", "rocket"), sorted(listdir(join(self.path, "spritesheets", "rocket"))), True)
        self.smoke_img = pg.image.load(join(self.path, "imgs", "smoke", "smoke.png")).convert_alpha()
        self.laser_img = pg.image.load(join(self.path, "imgs", "laser", "laser_beam.png")).convert_alpha()

    @staticmethod
    def prep_images(path, imgnames:list[str], counter_key=False) -> dict:
        out_dict = {}
        for i, imgname in enumerate(imgnames):
            if not counter_key:
                out_dict[imgname.split(".")[0]] = pg.image.load(join(path, imgname)).convert_alpha()
            else:
                out_dict[i] = pg.image.load(join(path, imgname)).convert_alpha()
        return out_dict

    def new(self):
        """ Called when game is initialized, can also be used for resetting the whole display. """
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()

        self.controller1 = Controller("wasd")

        for row, tiles in enumerate(self.map.map):
            for column, tile in enumerate(tiles):
                if tile != "." and tile != "p":
                    Wall([self.all_walls, self.all_sprites], column, row, self.textures[tile], tile)
                elif tile == "p":
                    self.player = Player(self, self.all_sprites, self.controller1, column, row, 10, 20, self.rocket_textures)

        self.camera = Camera(self.map.width, self.map.height)

    def update(self):   
        # update all groups
        self.all_sprites.update(self.all_walls)
        self.camera.update(self.player)

    def draw(self):
        # fill screen with background color
        self.screen.fill(BACKGROUND_COLOR)

        # Display FPS in caption
        pg.display.set_caption(f"{self.clock.get_fps():.2f}")
        
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()
    
    def reset(self, event):
        super().keypress_handler(event)
        key = pg.key.get_pressed()
        if key[pg.K_r]:
            self.new()
    
if __name__ == "__main__":
    # call on simulation, execute new and run to start main loop
    mayhem_clone = Main()
    while True:
        mayhem_clone.new()
        mayhem_clone.run()
