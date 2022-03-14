import pygame as pg
vec = pg.math.Vector2
pg.init()

screen = pg.display.set_mode((700, 700))

def collide(rect1, rect2):
    if rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y < rect2.y + rect2.height and rect1.height + rect1.y > rect2.y:
        if rect1.midtop[1] > rect2.midtop[1]:
            print("top")
            return (255, 0, 0)
        elif rect1.midbottom[1] < rect2.midbottom[1]:
            print("bottom")
            return (0, 255, 255)
        elif rect1.midleft[0] > rect2.midleft[0]:
            print("left")
            return (255, 255, 0)
        else:
            print("right")
            return (255, 0, 255)
    else:
        return (0, 0, 255)

while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
    img1 = pg.Surface((100, 100), pg.SRCALPHA)
    img2 = pg.Surface((50, 50), pg.SRCALPHA)
    rect1 = img1.get_rect(center = (700 // 2, 700 // 2))
    rect2 = img2.get_rect(center = pg.mouse.get_pos())


    color = collide(rect1, rect2)
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, (0, 255, 0), rect1)
    pg.draw.rect(screen, color, rect2)

    pg.display.flip()