""" 
A python module containing the Menu object.
"""

import pygame as pg

from .settings import *

class Menu:
    """ 
    A pygame menu object used for creating main menus, settings menus, pause menus, etc.

    Parameters:
        menu:
            Menu objects prefer having a main menu as a hub to other menus or starting a Main_loop object. Therefore if the menu you wish to set up is not the main menu object, specify menu=main_menu. Optional, default: None
        width, height: int, int
            Menu screen width and height. Optional, default: WIDTH, HEIGHT from imported settings module
        bg_color: Tuple(int, int, int)
            Color of menu screen

    Note: This object uses a settings module to get its screen width and height

    On execution self.load_data and self.interactives are called, therefore specify methods in child objects if needed.
    """
    def __init__(self, menu=None, width=1000, height=900, bg_color=(171, 214, 214)):
        
        # if parent/other menus exist
        self.menu = menu

        # other attributes
        self.width, self.height = width, height
        self.bg_color = bg_color

        # buttons
        self.all_interactives = []

        # display object
        self.screen = pg.display.set_mode((self.width, self.height))

        # load data and call interactives
        self.load_data()
        self.interactives()

    def load_data(self):
        pass

    def run(self):
        """ 
        Main update loop.

        Calls three methods each iteration: self.event_handling, self.interaction, self.draw
        """
        while True:
            self.event_handling()
            self.interaction()
            self.draw()

    def interactives(self):
        pass

    def interaction(self):
        """
        Update function for interactives.
        """
        for interactive in self.all_interactives:
            interactive.interaction()
        
    def draw(self):
        self.screen.fill(self.bg_color)
        
        # draw interactives.
        for interactive in self.all_interactives:
            interactive.draw()

        pg.display.flip()

    def event_handling(self):
        """
        Event handling
        """

        # event based approach, dont update unless event.
        self.event = pg.event.wait()
        if self.event.type == pg.QUIT:
            exit()
        elif self.event.type == pg.KEYDOWN:
            if self.event.key == pg.K_ESCAPE:
                if self.menu is not None:
                    self.menu.run()
                else:
                    exit()