import pygame as pg
from .event_handler import EventDispatcher, EventHandler, DuplicateHandlerError

# pygame init
pg.init()

class Loop:
    def __init__(self, width, height, fps):
        self.width, self.height = width, height
        self.fps = fps

        self.screen = pg.display.set_mode((self.width, self.height), 0, 32)

        # set up a game clock
        self.clock = pg.time.Clock()

        # list for containing all interactive objects
        self.all_interactives = []

        # load data
        self.load_data()
        
        # timer
        self.t = 0

        # setting up a event handling dispatcher
        self.dispatcher = EventDispatcher()
        
        # make a event handler for quitting
        self.quit_handler = EventHandler(pg.KEYDOWN)
        self.quit_handler.handler = self.keypress_handler
        self.dispatcher.register_handler(self.quit_handler)

    def load_data(self):
        """ Loads data when instanced. """
        pass

    def new(self):
        """ Starts a new game with a new counter, level 1, all obstacles, music and ball """
        pass

    def run(self):
        """ Continouously runs and checks for events and updates sprites and game logic as well as drawing sprites and background. """
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(self.fps) / 1000
            self.event_handling()
            self.update()
            self.draw()
            self.t += self.dt

    def update(self):
        """ Update once every frame """
        pass

    def draw(self):
        """ Draws once every frame """
        pass

    def quit(self):
        pg.quit()
        exit()

    def event_handling(self):
        for event in pg.event.get():
            # quit if exit button pressed
            if event.type == pg.QUIT:
                self.quit()
            else:
                self.dispatcher.dispatch(event) 
    
    def keypress_handler(self, event):
        key_input = pg.key.get_pressed()
        if key_input[pg.K_ESCAPE]:
            self.quit()
        if key_input[pg.K_q]:
            self.quit()
