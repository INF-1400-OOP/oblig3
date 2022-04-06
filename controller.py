""" This module contains the Controller class which can be instantiated with a argument deciding what keys to use for controls of the respective player object. 

TODO: Make a custom exception for when duplicate controls are registered.
"""

import pygame as pg 

class Controller:
    """ Controller class which is passed to a player object to give that object controls. This class should be used to avoid multiple player objects having the same controls. 
    
    Attributes
    ----------
    controller1, controller2 : dict, dict
        Two separate predefined controller dicts where keys are the pygame.K_insert_key and items are what methods to use when key is pressed.
    controllers : dict
        Dictionary containing the avaliable controllers. Keys are a string of what keys to use and items are controller1 or controller2 attributes.
    controls : dict
        What controller is in use
    
    Methods
    -------
    register_keystrokes()
        Include in update() of object which has control over this controller to register what to do on keystrokes.
    set_key_bindings(up, left, right, down)
        Register which functions to call when keys are pressed.

    TODO: Should add controller to a list of controllers in game object, then compare and ensure that controls are not duplicates
    """
    def __init__(self, in_use="wasd"):
        """
        Args
        ----
        in_use : str
            What controls to use. (default "wasd")
        """

        self.controller1 = {pg.K_w: self._up,
                            pg.K_a: self._left,
                            pg.K_d: self._right,
                            pg.K_s: self._down}
        self.controller2 = {pg.K_UP: self._up,
                            pg.K_LEFT: self._left,
                            pg.K_RIGHT: self._right,
                            pg.K_DOWN: self._down}

        self.controllers = {"wasd": self.controller1, "arrows": self.controller2}

        self.controls = self.controllers[in_use]

    def register_keystrokes(self):
        """ Method for registering when a predefined key is pressed and executing registered method of player class. Include this method in player's update(). """
        key = pg.key.get_pressed()

        for defined_key in self.controls.keys():
            if key[defined_key]:
                self.controls[defined_key]()

    def set_key_bindings(self, up, left, right, down):
        """ Method for setting what methods to call when register_keystrokes() register a keystroke. """
        self.up = up
        self.left = left
        self.right = right
        self.down = down
    
    def _up(self):
        """ Method for calling up """
        self.up()
    
    def _left(self):
        """ Method for calling left """
        self.left()
    
    def _right(self):
        """ Method for calling right """
        self.right()
    
    def _down(self):
        """ Method for calling down """
        self.down()
    