""" 
Module containing interactive objects which can be used in a Menu or game-loop object.

Requirements:
    python modules:
        settings.py:
            A file specifying colors and other settings.
        text.py:
            A file containing the draw_text function.
"""

import pygame as pg

vec = pg.math.Vector2

from game_base_module.settings import *
from game_base_module.text import *
from game_base_module.util import *

class Interactives:
    """ 
    A base-class for interactives.

    Requires a all_interactives list in menu object. Defined before object.

    Parameters:
        menu: Menu object
            A menu in which to draw the interactive object.
        x, y, width, height: int, int, int, int
            x and y specifies the center point to draw the interactive and place its rect object. width and height define the size of the pygame.Surface created.
        text: str
            Text which will be drawn in contention with the interactive object.
        color: tuple(int, int, int)
            Color. Optional. Default: (150, 150, 150).
        text_size: int
            Size of text. Optional. Default: 36.
    """
    def __init__(self, 
                menu, 
                x, 
                y, 
                text, 
                width=200, 
                height=40,
                color=LIGHT_GREY, 
                text_size=36
                ):
        self.menu = menu
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.color = color
        self.text_size = text_size
        self.text_color = BLACK
        self.text = text

        # create pygame surface
        self.image = pg.Surface((width, height), pg.SRCALPHA)

        # get a rect from surface, center on (x, y)
        self.rect = self.image.get_rect(center=(x, y))

        # add interactive to list of all interactives for easier updating.
        self.menu.all_interactives.append(self)

    def draw(self):
        pass

    def interaction(self):
        pass

class HealthBar(Interactives):
    def __init__(self, startval=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.greenimg = pg.Surface(vec(self.width, self.height), pg.SRCALPHA)
        self.greenrect = self.greenimg.get_rect(midleft=vec(self.x, self.y))
        self.rect = self.image.get_rect(midleft=vec(self.x, self.y))

        self.val = startval

    def interaction(self, new_val):
        self.val = new_val
        self.greenrect.width = map_val(self.val, 0, 100, 0, self.width)

    def draw(self):
        draw_text(self.menu.screen, self.text, self.text_size - 10, self.x, self.y-30, WHITE)
        pg.draw.rect(self.menu.screen, RED, self.rect)
        pg.draw.rect(self.menu.screen, GREEN, self.greenrect)


class TextBox(Interactives):
    """
    Text-box-object. Blits text on screen.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.visible_box = visible_box

    def draw(self):
        # if self.visible_box:
        #     pg.draw.rect(self.menu.screen, self.color, self.rect, border_radius=10)

        draw_text(self.menu.screen, self.text, self.text_size, self.x, self.y, self.text_color, center=True)

class Slider:
    """
    Slider object. Generates a slider centered at x, y stretching from x - width to x + width.

    Requires a all_interactives list in menu object. Defined before Slider object.

    Parameters:
        menu: Menu object
            A menu in which to draw the interactive object.
        x, y: int, int
            center of Slider at (x, y).
        text: str
            Text which will be drawn above the Slider object, sort of a description.
        val: int
            Value between 0 and 100 of how many percent the sliders default value should be. Optional, default 100.
        width, height: int, int
            Sliders rect is 2 * width, height. Optional, default width=100, height=10.
        color: tuple(int, int, int)
            color of slider. Optional, default (150, 150, 150).
        text_size: int
            Size of text. Optional. Default: 36.
    """
    def __init__(self,
                menu,
                x,
                y,
                text,
                val=100,
                width=100,
                height=10,
                color=LIGHT_GREY,
                text_size=36,
                ):
        self.menu = menu

        # define image
        self.image = pg.Surface((width * 2, height), pg.SRCALPHA)

        # get and set rect center to x, y
        self.rect = self.image.get_rect(center=(x, y))

        # declarations
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.text = text
        self.text_size = text_size
        self.val = val

        # add to all interactives list.
        self.menu.all_interactives.append(self)

        # set slider position
        self.slider_pos = self.calc_val(self.val, backwards=True)

        # define rect of slider circle
        self.mover_rect = pg.Rect(self.slider_pos, self.y - 5, 10, 10)

    def draw(self):
        # drawing the line
        pg.draw.line(self.menu.screen, self.color, vec(self.x - self.width, self.y), vec(self.x + self.width, self.y), width=3)
        
        # drawing the circle
        pg.draw.circle(self.menu.screen, DARK_GREY, self.mover_rect.center, 5)

        # Slider text
        draw_text(self.menu.screen, self.text, self.text_size, self.x, self.y - 20, BLACK, center=True)
        
        # Percentage value blitted on the right side of the line.
        draw_text(self.menu.screen, f"{self.get_val()}", self.text_size - 10, self.x + self.width + 30, self.y, BLACK, center=True)

    def interaction(self):
        """ Handles interactions """

        # check for mouseclicks
        if self.menu.event.type == pg.MOUSEBUTTONDOWN:

            mpos = pg.mouse.get_pos()

            # only store x position of mouse
            x = mpos[0]

            # checks if mpos collides with the rect over the drawn line
            if self.rect.collidepoint(mpos):

                # restrictions to x position
                x = min(self.x + self.width, x)
                x = max(self.x - self.width, x)

                # set mover rect center to varying x and constant y
                self.mover_rect.center = (int(x), self.y)

                # update slider position
                self.slider_pos = x
    
    def get_val(self) -> int:
        """ Updates val """
        self.val = self.calc_val(self.slider_pos)
        return self.val

    def calc_val(self, new_val, backwards=False) -> int:
        """
        Calculates the percentage value of a given x position in relation to objects rect. If backwards is set to True it is algebraically the same expression but solved for the position of the slider circle given a percentage value.

        Parameters:
            if backwards False:
                new_val: int
                    x position.
                Returns: int
                    Percentage value.
            if backwards True:
                new_val: int
                    Percentage value.
                Returns: int
                    x position
        """
        if not backwards:
            return int((new_val - self.x + self.width) / (self.width * 2) * 100)
        else:
            return int(2 * self.width * new_val / 100 + self.x - self.width)
        
class Button(Interactives):
    """
    Child class to Interactives. Handles, draws and updates buttons.

    Parameters:
        func: func
            The function to be executen when button is clicked.
        hover_color: tuple(int, int, int)
            Color to be displayed when mouse hovering over button.
    """
    def __init__(self, func=None, hover_color=GREY, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func = func
        self.hover_color = hover_color

    def draw(self):
        mpos = pg.mouse.get_pos()

        # check if mouse pos inside button box
        if self.rect.collidepoint(mpos[0], mpos[1]):
            # draw with hover_color
            pg.draw.rect(self.menu.screen, self.hover_color, self.rect, border_radius=10)
        else:
            # draw with regular color
            pg.draw.rect(self.menu.screen, self.color, self.rect, border_radius=10)

        # draws text inside of button
        draw_text(self.menu.screen, str(self.text), self.text_size, self.rect.center[0], self.rect.center[1], BLACK, center=True)

    def interaction(self):
        # check for mouse click event
        if self.menu.event.type == pg.MOUSEBUTTONDOWN:

            # check for collision between mouse and button
            if self.rect.collidepoint(self.menu.event.pos):

                # execute function
                self.func()

# class Button1:
#     def __init__(self, 
#                 menu, 
#                 x, 
#                 y, 
#                 text,
#                 func, 
#                 width=200, 
#                 height=40, 
#                 color=LIGHT_GREY, 
#                 text_size=36, 
#                 hover_color=GREY,
#                 pressed_text=None
#                 ):
#         self.menu = menu
#         self.image = pg.Surface((width, height), pg.SRCALPHA)
#         self.rect = self.image.get_rect(center = (x, y))
#         self.color = color
#         self.hover_color = hover_color
#         self.text = text
#         self.text_size = text_size
#         self.func = func
#         self.pressed_text = pressed_text
#         self.menu.all_interactives.append(self)

#     def draw(self):
#         mpos = pg.mouse.get_pos()

#         # check if mouse pos inside button box
#         if self.rect.collidepoint(mpos[0], mpos[1]):
#             pg.draw.rect(self.menu.screen, self.hover_color, self.rect, border_radius=10)
#         else:
#             pg.draw.rect(self.menu.screen, self.color, self.rect, border_radius=10)

#         self.text_he = draw_text(self.menu.screen, str(self.text), self.text_size, self.rect.center[0], self.rect.center[1], (0, 0, 0), center=True)
        
#     def interaction(self):
#         if self.menu.event.type == pg.MOUSEBUTTONDOWN:
#             if self.rect.collidepoint(self.menu.event.pos):
#                 self.func()