import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2

def randcol(min, max):
    """ Tilfeldig ish farge i på intervall (min, max] """
    return (randint(min, max), randint(min, max), randint(min, max))

def collide(rect1, rect2):
    """ Collision detection between two rectangles. If collision detected a integer boolean is returned as either 0 or 1 corresponding to a hit of top/bottom or left/right.
    
    Parameters:
        rect1: pygame.Rect(x, y, w, h)
            First rectangle
        rect2: pygame.Rect(x, y, w, h)
            Second rectangle
    Returns:
        if no collision:
            None
        if collison:
            1 - top/bottom
            0 - left/right
    """
    if rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y < rect2.y + rect2.height and rect1.height + rect1.y > rect2.y:
        if rect1.midtop[1] > rect2.midtop[1]:
            return 1

        elif rect1.midbottom[1] < rect2.midbottom[1]:
            return 1

        elif rect1.midleft[0] > rect2.midleft[0]:
            return 0
        else:
            return 0
    else:
        return False

def percent(val, of):
    return int(val / of * 100)

def map_val(x, from_min, from_max, to_min, to_max):
    """ Determine a value for x in from an initial [from_min, from_max] to a new [to_min, to_max] such that the relation is constant.
    
    Paramters:
        x: Scalar
            Value to be mapped.
        from_min: Scalar
            Smallest possible value in domain.
        from_max: Scalar
            Largest possible value in domain.
        to_min: Scalar
            Smallest possible value in codomain.
        to_max: Scalar
            Largest possible value in codomain.
    """
    val = (x - from_min) / (from_max - from_min)
    return (to_max - to_min) * val + to_min

def randvec(xmin, xmax, ymin, ymax):
    return vec(uniform(xmin, xmax), uniform(ymin, ymax))

if __name__ == '__main__':
    print(f"{map_val(90, 100, 0, 0, 100)}")