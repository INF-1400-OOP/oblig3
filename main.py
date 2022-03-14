import pygame as pg
from random import randint, uniform
from os import listdir
from os.path import join, dirname

from game_base_module import *
from config import *

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
        

    def load_data(self):
        pass

    def new(self):
        """ Called when game is initialized, can also be used for resetting the whole display. """
        pass

    def update(self):
        # update all groups
        pass

    def draw(self):
        # fill screen with background color
        self.screen.fill(BACKGROUND_COLOR)

        # Display FPS in caption
        pg.display.set_caption(f"{self.clock.get_fps():.2f}")

        pg.display.flip()
    
if __name__ == "__main__":
    # call on simulation, execute new and run to start main loop
    mayhem_clone = Main()
    while True:
        mayhem_clone.new()
        mayhem_clone.run()
