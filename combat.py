from pygame import draw
from settings import *
import pygame as py
from dokemon import *
import time

class Menu:
    def __init__(self, playerDokemon):
        self.options = ["Attk 1"]
        self.dokemon = playerDokemon
        self.selected = 0
        self.attks = self.dokemon.attks
        self.options = [self.attks[0], self.attks[1], self.attks[2], self.attks[3], ["bag", 0], ["item", 0], ["run", ]]

class MessagerLogger:
    def __init__(self):
        self.rawMessageList = []
        self.shownMessageList = []
    def logMessage(self, message):
        if(len(self.shownMessageList) >= 3):
            self.shownMessageList.append(message)
            self.shownMessageList.pop(0)
        else:
            self.shownMessageList.append(message)
    

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
        self.turnNum = 0

    def draw_text(self, text, font_name, size, color, x, y, surface):
        font = py.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.y = y
        text_rect.x = x
        surface.blit(text_surface, text_rect)

    def draw_health_Bar(self, x, y, pct):
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
        py.draw.rect(self.game.screen, col, fill_rect)
        py.draw.rect(self.game.screen, BLACK, outline_rect, 2)

    def initialize(self):
        self.player = Dokemon()
        self.player.name = "A"
        self.Oponent = Dokemon()
        self.Oponent.name = "B"
        self.messagerLogger = MessagerLogger()
        self.sprites = py.sprite.Group()

    
    def events(self):
        py.event.wait()
        waiting = True
        while waiting:
            self.update()
            self.draw()
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.game.quit()
                if event.type == py.KEYDOWN:
                    if event.key == py. K_DOWN or  event.key == py. K_s:
                        if self.menu.selected < 7:
                            self.menu.selected += 1
                    if event.key == py. K_UP or  event.key == py. K_w:
                        if self.menu.selected > -1:
                            self.menu.selected -= 1
                    if event.key == py. K_LEFT or  event.key == py. K_a:
                        self.menu.selected -= 3
                    if event.key == py. K_RIGHT or  event.key == py. K_d:
                        self.menu.selected += 3
                    if event.key == py. K_SPACE or event.key == py. K_RETURN:
                        stillAlive = self.player.decideAttacks(self.menu.selected, self.Oponent)
                        self.messagerLogger.logMessage(self.player.name + " used " + self.player.attks[self.menu.selected][0])
                        self.messagerLogger.logMessage(self.Oponent.name + " health decrease")
                        if not stillAlive:
                            self.messagerLogger.logMessage(self.Oponent.name + " is dead")
                        waiting = False
                        
                    if event.key == py.K_p:
                        self.paused = not self.paused
                    
                    if self.menu.selected > 6:
                        self.menu.selected = 6
                    if self.menu.selected < 0:
                        self.menu.selected = 0

    def decideturn(self):
        if self.Oponent.speed > self.player.speed:
            self.playerFirst = False
        elif self.Oponent.speed < self.player.speed:
            self.playerFirst = True
        else:
            choice = rd.randint(0,1)
            if choice == 1:
                self.playerFirst = True
            else:
                self.playerFirst = False

    def turn(self):
        if self.turnNum % 2 == 0:
            if self.playerFirst:
                self.events()
            else:
                stillAlive = self.Oponent.decideRandAttack(self.player)

                self.messagerLogger.logMessage(self.player.name + " used " + self.Oponent.attks[self.menu.selected][0])
                self.messagerLogger.logMessage(self.Oponent.name + " health decrease")
                if not stillAlive:
                    self.messagerLogger.logMessage(self.Oponent.name + " is dead")
        else:
            if self.playerFirst:
                stillAlive = self.Oponent.decideRandAttack(self.player)
                self.messagerLogger.logMessage(self.player.name + " used " + self.player.attks[self.menu.selected][0])
                self.messagerLogger.logMessage(self.Oponent.name + " health decrease")
                if not stillAlive:
                    self.messagerLogger.logMessage(self.Oponent.name + " is dead")
            else:
                self.events()
        self.turnNum += 1

    def run(self):
        # game loop - set self.playing = False to end the game
        self.initialize()
        firstLoop = True
        self.playing = True
        while self.playing:
            if(firstLoop):
                self.update()
                self.draw()
                firstLoop = False
            self.decideturn()
            self.dt = self.game.clock.tick(FPS) / 1000
            self.turn()
            if not self.paused:
                self.update()
            self.draw()

    def draw(self):
        y = 610
        x = 520
        for i in self.menu.options:
            if(i[0] == "bag"):
                x += 150
                y = 610
            if self.menu.options[self.menu.selected] == i:
                self.draw_text( i[0] , self.game.title_font, TEXTSIZE, YELLOW, x, y, self.game.screen)
            else:
                self.draw_text( i[0], self.game.title_font, TEXTSIZE, BLACK, x, y, self.game.screen)
            y += 35
        self.draw_text( self.player.name , self.game.title_font, TEXTSIZE, BLACK, 150, 125, self.game.screen)
        self.draw_health_Bar(150, 150, self.player.health / self.player.maxHealth)
        self.draw_text( self.Oponent.name , self.game.title_font, TEXTSIZE, BLACK, 500, 75, self.game.screen)
        self.draw_health_Bar( 500, 100, self.Oponent.health / self.Oponent.maxHealth)
        x = 100
        y = 610
        for message in self.messagerLogger.shownMessageList:
            self.draw_text(message, self.game.title_font, TEXTSIZE, BLACK, x, y, self.game.screen)
            y += 35
        py.display.flip()

    def update(self):
        py.display.set_caption("{:.2f}".format(self.game.clock.get_fps()))
        self.game.screen.blit(self.capture_background, (0, 0))
        self.sprites.update()