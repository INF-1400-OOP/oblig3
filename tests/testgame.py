import pygame as pg
from map import Map
from settings import *
from camera import Camera
pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT), 0, 32)

clock = pg.time.Clock()

map = Map("testmap.txt")

class Wall(pg.sprite.Sprite):
    def __init__(self, group, x, y):
        # self.groups = group1, group2
        super().__init__(group)
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        self.image.fill((255, 182, 193))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Player(pg.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pg.Surface((10, 20), pg.SRCALPHA)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            self.rect.y -= 5
        if key[pg.K_s]:
            self.rect.y += 5
        if key[pg.K_a]:
            self.rect.x -= 5
        if key[pg.K_d]:
            self.rect.x += 5

def update():
    walls.update()
    sprites.update()
    camera.update(player)

def draw(screen):
    screen.fill((60, 60, 60))
    # screen.blit(bgimg, (0,0))

    for sprite in sprites:
        screen.blit(sprite.image, camera.apply(sprite))
    
    pg.display.flip()

# bgimg = pg.image.load("iu.jpeg").convert_alpha()

sprites = pg.sprite.Group()
walls = pg.sprite.Group()
for row, tiles in enumerate(map.map):
    for col, tile in enumerate(tiles):
        if tile == "1":
            Wall([walls, sprites], col, row)
        if tile == "p":
            player = Player(sprites, col, row)

camera = Camera(map.width, map.height)
while True:
    dt = clock.tick(60) / 1000
    update()
    draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            key = pg.key.get_pressed()
            if key[pg.K_q]:
                pg.quit()
                exit()
