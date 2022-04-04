import pygame as pg
import numpy as np
from os import listdir
from os.path import join, dirname

from game_base_module import *
from config import *
from camera import Camera
from map import Map, Screen
from sprites import Wall
from player import Player
from controller import Controller
from scoreboard import Scoreboard

vec = pg.math.Vector2

class Main(Loop):
    def __init__(self):
        # set path to main file
        self.path = dirname(__file__)

        # set path to directory containing textures.
        self.texturedir = join(self.path, "textures")

        # super Loop object
        super().__init__(WIDTH, HEIGHT, FPS)

        self.screen1 = Screen(0, 0, self.width // 2, self.height)
        self.screen2 = Screen(self.width // 2, 0, self.width // 2, self.height)

        # set center of screen
        self.center = vec(self.width // 2, self.height // 2)

        self.resethandler = EventHandler(pg.KEYDOWN)
        self.resethandler.handler = self.reset
        self.dispatcher.register_handler(self.resethandler)

    def load_data(self):
        self.map = Map("testmap1.txt")
        self.textures = self.load_img_to_dict(join(self.texturedir, "blocks"))
        self.rocket_textures = self.load_img_to_dict(join(self.texturedir, "rocket"), True, True)
        self.smoke_img = pg.image.load(join(self.texturedir, "smoke", "smoke.png")).convert_alpha()
        self.laser_img = pg.image.load(join(self.texturedir, "laser", "laser_beam.png")).convert_alpha()
        self.explotion_img = self.load_img_to_list(join(self.texturedir, "explotion"), sort=True)
        self.background = pg.image.load(join(self.texturedir, "background", "test_background.png")).convert_alpha()

    @staticmethod
    def load_img_to_dict(path_to_dir, counter_key=False, sort=False) -> dict:
        imgs = listdir(path_to_dir)

        if sort:
            imgs = sorted(listdir(path_to_dir))

        if counter_key:
            keys = range(0, len(imgs))
            return {i:pg.image.load(join(path_to_dir, im)).convert_alpha() for (i, im) in zip(keys, imgs)}

        imname = [name.split(".")[0] for name in imgs]
        return {name:pg.image.load(join(path_to_dir, im)).convert_alpha() for (name, im) in zip(imname,imgs)}

    @staticmethod
    def load_img_to_list(path_to_dir, sort=False):
        if sort:
            return [pg.image.load(join(path_to_dir, im)).convert_alpha() for im in sorted(listdir(path_to_dir))]
        return [pg.image.load(join(path_to_dir, im)).convert_alpha() for im in listdir(path_to_dir)]

    def new(self):
        """ Called when game is initialized, can also be used for resetting the whole display. """
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.all_players = pg.sprite.Group()
        self.all_statuses = pg.sprite.Group()

        self.controller1 = Controller("wasd")
        self.controller2 = Controller("arrows")

        self.scoreboard = Scoreboard()

        for row, tiles in enumerate(self.map.map):
            for column, tile in enumerate(tiles):
                if tile != "." and tile != "1" and tile != "2":
                    Wall([self.all_walls, self.all_sprites], column, row, self.textures[tile], tile)
                elif tile == "1":
                    self.player1 = Player(self, self.controller1, column, row, self.rocket_textures, 1, self.screen1)
                elif tile == "2":
                    self.player2 = Player(self, self.controller2, column, row, self.rocket_textures, 2, self.screen2)

        self.camera1 = Camera(self.map.width, self.map.height)
        self.camera2 = Camera(self.map.width, self.map.height)


    def update(self):
        # update all groups
        self.all_sprites.update(self.all_walls)
        self.all_statuses.update()
        self.camera1.update(self.player1)
        self.camera2.update(self.player2)

    def draw(self):
        # fill screen with background color
        self.screen1.surf.fill(BACKGROUND_COLOR)
        self.screen2.surf.fill(BACKGROUND_COLOR)

        # Display FPS in caption
        pg.display.set_caption(f"{self.clock.get_fps():.2f}")
        
        for sprite in self.all_sprites:
            self.screen1.surf.blit(sprite.image, self.camera1.apply(sprite.rect))
            self.screen2.surf.blit(sprite.image, self.camera2.apply(sprite.rect))

        self.screen.blit(self.screen1.surf, self.screen1.rect)
        self.screen.blit(self.screen2.surf, self.screen2.rect)

        pg.draw.line(self.screen, BLACK, (self.width // 2, 0), (self.width //2,self.height), 5)

        self.all_statuses.draw(self.screen)

    def reset(self, event):
        super().keypress_handler(event)
        key = pg.key.get_pressed()
        if key[pg.K_r]:
            self.new()

    def respawn(self, player_n, lp_rect):
        if player_n == 1:
            self.player1 = Player(self, self.controller1, 0,0, self.rocket_textures, 1, self.screen1)
            self.player1.rect.midbottom = lp_rect.midtop
            self.player1.pos = vec(self.player1.rect.center)
            self.scoreboard.give_point("2")
        elif player_n == 2:
            self.player2 = Player(self, self.controller2, 0,0, self.rocket_textures, 2, self.screen2)
            self.player2.rect.midbottom = lp_rect.midtop
            self.player2.pos = vec(self.player2.rect.center)
            self.scoreboard.give_point("1")

        print(self.scoreboard)


if __name__ == "__main__":
    # call on simulation, execute new and run to start main loop
    mayhem_clone = Main()
    while True:
        mayhem_clone.new()
        mayhem_clone.run()
