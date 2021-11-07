from pygame import draw
from settings import *
import pygame as py
from dokemon import *
import random as rd
import time

class Menu:
    def __init__(self, playerDokemon):
        self.options = []
        self.dokemon = playerDokemon
        self.selected = 0
        self.moves = self.dokemon.moves
        for i in self.moves:
            self.options.append(i)
        self.options.extend([["bag", 0], ["run", 0]])

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

class Items:
    def __init__(self):
        self.name = 0
        self.messsage = MessagerLogger()
    def heal(self, user):
        user.health += (0.3 * user.maxHealth)
        self.messsage.logMessage("You abilied a healing kit")
        self.messsage.logMessage(user.name + " healed to  " + user.health + " hp")

class Dokeball:
    def __init__(self):
        self.name = 0
        self.message = MessagerLogger()
    def throw(self, user, target):
        chance = rd.randint(0, 50) - (target.health / target.maxHealth)
        if (chance < 25):
            self.message.logMessage(target.name + " has been caught")
            user.bag.append(target)
        else:
            self.message.logMessage(target.name + " escapes the ball")

class Combat:
    def __init__(self, game):
        #class declare for wild dokemon
        self.wild_dokemon = None
        self.capture_background = game.combatBackground
        self.sprites = py.sprite.Group()
        for dokemon in data['possibleDokemon']:
            #dumby vals
            movesList = []
            name = str(dokemon['name'])
            
            for stats in dokemon['stats']:
                health = int(stats['health'])
                defense = int(stats['defense'])
                speed = int(stats['speed'])
                sp_attack = int(stats['sp. attack'])
                sp_defense = int(stats['sp. defense'])
                attack = int(stats['attack'])
            for moves in dokemon['moves']:
                # add damage mod here
                moveName = str(moves['moveName'])
                number = moves['id']
                movesList.append((moveName, number))
            for images in dokemon['images']:
                image = images["sprite"]
                print("image:" + image)
            animal = Dokemon(name, health, sp_defense, sp_attack, defense, speed, attack, movesList, self, game, image)
            dokemonList.append(animal)
        self.menu = Menu(dokemonList[1])
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
        # what 
        self.player = dokemonList[0]
        self.player.name = "Gerald"
        self.Oponent = dokemonList[1]
        self.Oponent.name = "Drake"
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
                        self.menu.selected += 1
                    if event.key == py. K_UP or  event.key == py. K_w:
                        self.menu.selected -= 1
                    if event.key == py. K_LEFT or  event.key == py. K_a:
                        self.menu.selected -= 3
                    if event.key == py. K_RIGHT or  event.key == py. K_d:
                        self.menu.selected += 3
                    if event.key == py. K_SPACE or event.key == py. K_RETURN:
                        stillAlive = self.player.decideAttacks(self.menu.selected, self.Oponent)
                        self.messagerLogger.logMessage(self.player.name + " used " + str(self.player.moves[self.menu.selected]))
                        if not stillAlive:
                            self.messagerLogger.logMessage(self.Oponent.name + " has fainted")
                        waiting = False
                        
                    if event.key == py.K_p:
                        self.paused = not self.paused
                    
                    if self.menu.selected > len(self.menu.options) - 1:
                        self.menu.selected = 5
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

                self.messagerLogger.logMessage(self.player.name + " used " + self.Oponent.moves[self.menu.selected][0])
                self.messagerLogger.logMessage(self.Oponent.name + " health decrease")
                if not stillAlive:
                    self.messagerLogger.logMessage(self.Oponent.name + " is dead")
        else:
            if self.playerFirst:
                stillAlive = self.Oponent.decideRandAttack(self.player)
                self.messagerLogger.logMessage(self.player.name + " used " + self.player.moves[self.menu.selected][0])
                self.messagerLogger.logMessage(self.Oponent.name + " health decrease")
                if not stillAlive:
                    self.messagerLogger.logMessage(self.Oponent.name + " has fainted")
                    
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
        y = 450
        x = 520
        for i in self.menu.options:
            if(i[0] == "bag"):
                x += 350
                y = 500
            if self.menu.options[self.menu.selected] == i:
                self.draw_text( i[0] , self.game.title_font, TEXTSIZE, YELLOW, x, y, self.game.screen)
            else:
                self.draw_text( i[0], self.game.title_font, TEXTSIZE, BLACK, x, y, self.game.screen)
            y += 55
        self.draw_text( self.player.name , self.game.title_font, TEXTSIZE, BLACK, 800, 300, self.game.screen)
        self.draw_health_Bar(800, 338, int(self.player.health) / int(self.player.health))
        self.draw_text( self.Oponent.name , self.game.title_font, TEXTSIZE, BLACK, 265, 62, self.game.screen)
        self.draw_health_Bar(265, 100, int(self.Oponent.health) / int(self.Oponent.health))
        x = 50
        y = 450
        for message in self.messagerLogger.shownMessageList:
            self.draw_text(message, self.game.title_font, TEXTSIZE, BLACK, x, y, self.game.screen)
            y += 35
        py.display.flip()

    def update(self):
        py.display.set_caption("{:.2f}".format(self.game.clock.get_fps()))
        self.game.screen.blit(self.capture_background, (0, 0))
        self.sprites.update()