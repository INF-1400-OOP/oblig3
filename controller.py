import pygame as pg 

class Controller:
    def __init__(self, in_use="wasd"):
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

        # self.up = None
        # self.down = None
        # self.left = None
        # self.right = None

    def register_keystrokes(self):
        key = pg.key.get_pressed()

        for defined_key in self.controls.keys():
            if key[defined_key]:
                self.controls[defined_key]()

    def set_key_bindings(self, up, left, right, down):
        self.up = up
        self.left = left
        self.right = right
        self.down = down
    
    def _up(self):
        self.up()
    
    def _left(self):
        self.left()
    
    def _right(self):
        self.right()
    
    def _down(self):
        self.down()
    