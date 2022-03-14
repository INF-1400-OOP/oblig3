import pygame as pg
vec = pg.math.Vector2
pg.init()

screen = pg.display.set_mode((400, 400))

widthred = 100
widthgreen = 100

clock = pg.time.Clock()

while True:
    dt = clock.tick(60) / 1000


    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    img1 = pg.Surface((widthred, 10), pg.SRCALPHA)
    img2 = pg.Surface((widthgreen, 10), pg.SRCALPHA)

    rect1 = img1.get_rect(center = vec(250, 350))
    rect2 = img2.get_rect(center = vec(250, 350))

    if widthgreen >= 1:
        widthgreen -= 10 * dt

    screen.fill((50, 50, 50))
    pg.draw.rect(screen, (255, 0, 0), rect1)
    pg.draw.rect(screen, (0, 255, 0), rect2)

    pg.display.flip()