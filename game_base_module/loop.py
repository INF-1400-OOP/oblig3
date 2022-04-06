import pygame as pg
from .event_handler import EventDispatcher, EventHandler, DuplicateHandlerError

# pygame init
pg.init()

class Loop:
    """ Base object for simple creation of game loops.
    
    Attributes
    ----------
    width, height : int, int
        Measurements of main display
    fps : int
        Target Frames Per Second of loop.
    screen : pg.Surface
        Main screen.
    clock : pygame.time.Clock
        Clock for synchronizing all in-game events and sprite movement.
    all_interactives : list
        List to keep track of interactives, like buttons, sliders and such if any.
    t : float
        Time since main loop start. (Default 0)
    dispatcher : EventDispatcher
        Dispatches events to EventHandler's when events occur.
    quit_handler : EventHandler
        Handles quitting.

    Methods
    -------
    load_data()
        Loads data when instanced.
    new()
        Starts a new game by instantiating all objects again.
    run()
        Continouously runs and checks for events and updates sprites and game logic as well as drawing sprites and background.
    update()
        Update all groups.
    draw()
        Draw all groups.
    quit()
        Quit game.
    event_handling()
        Handle events using EventDispatcher.
    keypress_handler(event)
        Handles keypresses and is attached to an EventHandler.
    """
    def __init__(self, width, height, fps):
        """
        Args
        ----
        width : int
            Screen width.
        height : int
            Screen height.
        fps : int
            Target fps.
        """
        self.width, self.height = width, height
        self.fps = fps
        
        self.screen = pg.display.set_mode((self.width, self.height))

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
            pg.display.flip()
            self.t += self.dt

    def update(self):
        """ Update once every frame. """
        pass

    def draw(self):
        """ Draws once every frame. """
        pass

    def quit(self):
        """ Quit game. """

        pg.quit()
        exit()

    def event_handling(self):
        """ Handle events using EventDispatcher. """

        for i, event in enumerate(pg.event.get()):
            # quit if exit button pressed
            if event.type == pg.QUIT:
                self.quit()
            else:
                self.dispatcher.dispatch(event)
                # print(i, event)
    
    def keypress_handler(self, event):
        """ Handles keypresses and is attached to an EventHandler. """

        key_input = pg.key.get_pressed()
        if key_input[pg.K_ESCAPE]:
            self.quit()
        if key_input[pg.K_q]:
            self.quit()
