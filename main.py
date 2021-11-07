import pygame as py
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from combat import *
import random as rand



# Colors
white = (255, 255, 255)

playing = False
helpScreen = False

# HUD functions
# def draw_player_health(surf, x, y, pct):
#     if pct < 0:
#         pct = 0
#     BAR_LENGTH = 100
#     BAR_HEIGHT = 20
#     fill = pct * BAR_LENGTH
#     outline_rect = py.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
#     fill_rect = py.Rect(x, y, fill, BAR_HEIGHT)
#     if pct > 0.6:
#         col = GREEN
#     elif pct > 0.3:
#         col = YELLOW
#     else:
#         col = RED
#     py.draw.rect(surf, col, fill_rect)
#     py.draw.rect(surf, WHITE, outline_rect, 2)
# def draw_player_ammo(surf, x, y, pct):
#     if pct < 0:
#         pct = 0
#     BAR_LENGTH = 100
#     BAR_HEIGHT = 20
#     fill = pct * BAR_LENGTH
#     outline_rect = py.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
#     fill_rect = py.Rect(x, y, fill, BAR_HEIGHT)
#     col = RED
#     py.draw.rect(surf, col, fill_rect)
#     py.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        py.mixer.pre_init(44100, -16, 1, 2048)
        py.init()
        self.screen = py.display.set_mode((WIDTH, HEIGHT))
        py.display.set_caption(TITLE)
        self.clock = py.time.Clock()
        self.combat = False
        self.start = True
        self.world = True
        self.capture = False
        self.end = False
        py.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align='nw'):
        font = py.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        outlineFont = py.font.Font(font_name, size)
        text_surface = outlineFont.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'nw':
            text_rect.topleft = (x, y)
        if align == 'ne':
            text_rect.topright = (x, y)
        if align == 'sw':
            text_rect.bottomleft = (x, y)
        if align == 'se':
            text_rect.bottomright = (x, y)
        if align == 'nw':
            text_rect.topleft = (x, y)
        if align == 'n':
            text_rect.midtop = (x, y)
        if align == 's':
            text_rect.midbottom = (x, y)
        if align == 'e':
            text_rect.midright = (x, y)
        if align == 'w':
            text_rect.midleft = (x, y)
        if align == 'center':
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def load_data(self):
        game_folder = path.dirname(__file__)
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'POKEMON.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.TTF')
        self.dim_screen = py.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map = TiledMap(path.join(self.map_folder, 'jungle.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.combatBackground = py.image.load(path.join(img_folder,'combatBackground.png'))
    
        self.player_img = py.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = py.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = py.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = py.sprite.LayeredUpdates()
        self.walls = py.sprite.Group()
        self.mobs = py.sprite.Group()
        self.wild_areas = py.sprite.Group()
        self.npcs = py.sprite.Group()
        self.items = py.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'jungle.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player  = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'wildArea':
                Wild_Area(self, tile_object.
                x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'npc':
                NPC(self, obj_center.x, obj_center.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
    

    def quit(self):
        py.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over?
        #if len(self.mobs) == 0:
            #self.playing = False
        # player hits items
        # hits = py.sprite.spritecollide(self.player, self.items, False)
        # for hit in hits:
        #     if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
        #         hit.kill()
        #         self.effects_sounds['health_up'].play()
        #         self.player.add_health(HEALTH_PACK_AMOUNT)
        #     if hit.type == 'shotgun':
        #         hit.kill()
        #         self.effects_sounds['gun_pickup'].play()
        #         self.player.weapon = 'shotgun'
        # mobs hit player  
        # bullets hit mobs

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            py.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            py.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        py.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, NPC):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                py.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                py.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)
         #HUD functions
        #self.draw_text('ammo', self.hud_font, 30, WHITE,  110, 30,)
        #self.draw_text('health', self.hud_font, 30, WHITE, 110, 0, )
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align='center')
        py.display.flip()

    def events(self):
        # catch all events here
        for event in py.event.get():
            if event.type == py.QUIT:
                self.quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.quit()
                if event.key == py. K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == py.K_p:
                    self.paused = not self.paused

    def combat_screen(self):
        combat = Combat(self)
        combat.run()
    def capture_screen(self):
        pass
    def show_start_screen(self):
        py.display.set_caption(TITLE)
        self.screen.fill(WHITE)
        self.draw_text('Press any key to Play', self.title_font, 75, RED, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Press H for Help', self.title_font, 75, RED, WIDTH / 2, HEIGHT * 3 / 4, align='center')
        self.draw_text('Dokemon South', self.title_font, 101, BLUE, WIDTH/2, HEIGHT / 2 - 100, align='center')
        self.draw_text("Dokemon South", self.title_font, 100, YELLOW, WIDTH /2, HEIGHT / 2 - 100, align='center')
        py.display.update()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3/ 4, align='center')
        py.display.flip()
        self.wait_for_key()

    def show_help_screen(self):
        self.screen.fill(WHITE)
        self.draw_text("Press escape to quit", self.title_font, 30, RED, WIDTH / 2, HEIGHT * .1, align='center')
        self.draw_text("Use arrow keys or wasd to move", self.title_font, 30, RED, WIDTH /2, HEIGHT *3/ 4, align='center')
        py.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        global playing, helpScreen
        py.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in py.event.get():
                if event.type == py.QUIT:
                    waiting = False
                    self.quit()
                if event.type == py.KEYUP:
                    waiting = False
                if event.type == py.KEYDOWN and event.key != py.K_ESCAPE and event.key != py.K_h:
                    playing = True
                if event.type == py.KEYDOWN and event.key == py.K_h:
                    helpScreen = True
                if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                    if helpScreen == True:
                        helpScreen = False
                    elif playing == True:
                        playing = False
                    else:
                        py.quit()
                        sys.exit()

# create the game object
g = Game()



while True:
    g.show_start_screen()
    while helpScreen == True:
        g.show_help_screen()


    while playing == True:
        if g.start:
            g.new()
            g.start = False
        if g.world:
            g.run()
            g.world = False
        if g.combat:
            g.combat_screen()
            g.combat = False
        if g.end:
            g.show_go_screen()
            g.end = False
