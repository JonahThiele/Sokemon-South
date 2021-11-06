from settings import *
import pygame as py
from dokemon import *

class Menu:
    def __init__(self, playerDokemon):
        self.options = ["Attk 1"]
        self.dokemon = playerDokemon
        self.selected = 0
        self.attack1 = self.dokemon.attk1
        self.attack2 = self.dokemon.attk2
        self.attack3 = self.dokemon.attk3
        self.attack4 = self.dokemon.attk4
        self.options = [self.attack1[0], self.attack2[0], self.attack3[0], self.attack4[0], "bag", "item", "run"]
    

class Combat:
    def __init__(self, game):
        #class declare for wild dokemon
        self.wild_dokemon = None
        self.capture_background = game.combatBackground
        #dumby vals
        self.sprites = py.sprite.Group()
        animal = Dokemon()
        self.menu = Menu(animal)
        self.paused = False
        self.game = game

    def draw_text(self, text, font_name, size, color, x, y, surface):
        font = py.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.y = y
        text_rect.x = x
        surface.blit(text_surface, text_rect)

    def draw_health_Bar(surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = py.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = py.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        py.draw.rect(surf, col, fill_rect)
        py.draw.rect(surf, BLACK, outline_rect, 2)

    def attack(self, attacker, defender, damage):
        pass
    def initialize(self):
        self.sprites = py.sprite.Group()
        self.draw_text("Combat initialized", self.game.title_font, 20, BLACK, WIDTH / 2, HEIGHT - 10, self.game.screen)

    
    def events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.game.quit()
            if event.type == py.KEYDOWN:
                if event.key == py. K_DOWN or  event.key == py. K_s:
                    self.menu.selected += 1
                if event.key == py. K_UP or  event.key == py. K_w:
                    self.menu.selected -= 1
                if event.key == py. K_LEFT or  event.key == py. K_a:
                    self.menu.selected -= 3
                if event.key == py. K_RIGHT or  event.key == py. K_d:
                    self.menu.selected += 3
                    
                if event.key == py.K_p:
                    self.paused = not self.paused
                
                if self.menu.selected > 6:
                    self.menu.selected = 6
                if self.menu.selected < 0:
                    self.menu.selected = 0

    def run(self):
        # game loop - set self.playing = False to end the game
        firstLoop = True
        self.playing = True
        while self.playing:
            if(firstLoop):
                self.update
            self.events()
            self.dt = self.game.clock.tick(FPS) / 1000
            if not self.paused:
                self.update()
            self.draw()

    def draw(self):
        y = 610
        x = 520
        for i in self.menu.options:
            if(i == "bag"):
                x += 150
                y = 610
            if self.menu.options[self.menu.selected] == i:
                self.draw_text( i , self.game.title_font, TEXTSIZE, YELLOW, x, y, self.game.screen)
            else:
                self.draw_text( i , self.game.title_font, TEXTSIZE, BLACK, x, y, self.game.screen)
            y += 35
        py.display.flip()

    def update(self):
        py.display.set_caption("{:.2f}".format(self.game.clock.get_fps()))
        self.game.screen.blit(self.capture_background, (0, 0))
        self.sprites.update()
     
