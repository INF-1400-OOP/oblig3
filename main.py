import pygame as pg
from random import randint, uniform
from os import listdir
from os.path import join, dirname

from game_base_module import *
from config import *
from camera import Camera

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

        # self.keypress_handler(pg.KEYDOWN)
        # self.keypress_handler.handler = keypress
        # self.dispatcher.register_handler(self.keypress_handler)

    def load_data(self):
        self.bg = pg.image.load("iu.jpeg").convert_alpha()
        self.bg_rect = self.bg.get_rect()

    def new(self):
        """ Called when game is initialized, can also be used for resetting the whole display. """
        self.all_sprites = pg.sprite.Group()
        self.p = Mover(self)
        # self.camera = Camera(self.bg_rect.width, self.bg_rect.height)
        self.camera = Camera(self.bg_rect.width, self.bg_rect.height)

    def update(self):
        # update all groups
        self.all_sprites.update()
        self.camera.update(self.p)

    def draw(self):
        # fill screen with background color
        # self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(self.bg, (0,0))

        # Display FPS in caption
        pg.display.set_caption(f"{self.clock.get_fps():.2f}")
        
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # self.all_sprites.draw(self.screen)
        pg.display.flip()
   
class Mover(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.image = pg.Surface((50, 50), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=game.center)
        self.image.fill(GREEN)
    
    def update(self):
        self.rect = self.image.get_rect()
        
        # self.rect.center = pg.mouse.get_pos()

    def draw(self, surf):
        pass


if __name__ == "__main__":
    # call on simulation, execute new and run to start main loop
    mayhem_clone = Main()
    while True:
        mayhem_clone.new()
        mayhem_clone.run()
