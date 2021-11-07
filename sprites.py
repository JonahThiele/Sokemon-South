import pygame as py
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from itertools import chain
from math import atan2, pi
import random as rd
vec = py.math.Vector2

def strip_from_sheet(sheet, start, size, columns, rows=1):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(py.Rect(location,size)))
    return frames

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = py.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = py.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_with_dokemon(sprite, group, game):
    hits = py.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        chance = rd.randint(0, 20)
        if chance == 20:
            game.combat = True
            game.playing = False


def collide_with_npc(sprite, group, game):
    hits = py.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        game.combat = True



class Player(py.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.health = PLAYER_HEALTH
        self.bag = []
        self.walk_state = 0
        self.last_dir = "None"


    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = py.key.get_pressed()
        mouse_buttons = py.mouse.get_pressed()
        if keys[py.K_UP] or keys[py.K_w]:
            if not self.last_dir == "up" or self.walk_state == 3:
                self.walk_state = 0
            self.vel = vec(0, -PLAYER_SPEED)
            return "up"
        if keys[py.K_DOWN] or keys[py.K_s]:
            if not self.last_dir == "down" or self.walk_state == 3:
                self.walk_state = 0
            self.vel = vec(0, PLAYER_SPEED)
            return "down"
        if keys[py.K_RIGHT] or keys[py.K_d]:
            if not self.last_dir == "right" or self.walk_state == 3:
                self.walk_state = 0
            self.vel = vec(PLAYER_SPEED, 0)
            return "right"
        if keys[py.K_LEFT] or keys[py.K_a]:
            if not self.last_dir == "left" or self.walk_state == 3:
                self.walk_state = 0
            self.vel = vec(-PLAYER_SPEED, 0)
            return "left"

    def rotate(self, dir):
        # mouse = py.mouse.get_pos()
        # mouse_x, mouse_y = mouse[0] - self.game.camera.x , mouse[1] - self.game.camera.y
        # rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        # self.rot = ((180 / pi) * -atan2(rel_y, rel_x)) % 360
        if( dir == "up"):
            self.rot = 90
        elif( dir == "down"):
            self.rot = 270
        elif( dir == "left"):
            self.rot = 180
        elif( dir == "right"):
            self.rot = 0
        
        self.image = py.transform.rotate(self.game.player_img, self.rot)

    def update(self):
        dir = self.get_keys()
        self.last_dir = dir
        self.image = self.game.player_images[self.walk_state]
        self.rotate(dir)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        collide_with_dokemon(self, self.game.wild_areas, self.game)
 

class Wall(py.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Wild_Area(py.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = WILD_AREA_LAYER
        self.groups = game.wild_areas
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #set to the size of tile
        self.rect =  py.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y 


class NPC(py.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = NPC_LAYER
        self.groups = game.all_sprites, game.npcs
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #set to the size of tile
        self.image = py.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(py.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = py.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y