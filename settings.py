import pygame as py
vec = py.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (106, 55, 5)


# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 683  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Sokemon South"
BGCOLOR = BROWN

TILESIZE = 64

GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'basic_snail.png'
PLAYER_HIT_RECT = py.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Mob settings

# Effects

# Layers
WALL_LAYER = 1
NPC_LAYER = 6
WILD_AREA_LAYER = 5 
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# encounter ssettings
TEXTSIZE = 35
OTHERSIZE = 30
