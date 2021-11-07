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
        self.messsage.logMessage("You applied a healing kit")
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
        self.last_turn = 0
        self.turn_delay = 500
        for dokemon in data['possibleDokemon']:
            #dumby vals
            movesList = []
            powerList = []
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
                power = int(moves['details'][0]['power'])
                powerList.append(power)

            for images in dokemon['images']:
                image = images["sprite"]
            
            animal = Dokemon(name, health, sp_defense, sp_attack, defense, speed, attack, movesList, self, game, image, powerList)
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
        BAR_LENGTH = 300
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = py.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = py.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.6 and pct <= 1:
            col = GREEN
        elif pct > 0.3 and pct <= 0.6:
            col = YELLOW
        else:
            col = RED
        py.draw.rect(self.game.screen, col, fill_rect)
        py.draw.rect(self.game.screen, BLACK, outline_rect, 2)

    def initialize(self):
        # what 
        choice = rd.randint(0, len(dokemonList) - 1)

        self.player = dokemonList[0]
        self.player.name = dokemonList[0].name
        self.opponent = dokemonList[choice]
        self.opponent.name = dokemonList[choice].name

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
                        if self.menu.selected <= 3:
                            stillAlive = self.player.decideAttacks(self.opponent, self.menu.selected, self.player)
                            self.messagerLogger.logMessage(self.player.name + " used " + self.player.moves[self.menu.selected][0])
                            waiting = False
                            if stillAlive == False:
                                self.messagerLogger.logMessage(self.opponent.name + " has died")
                                self.game.player.completed_comp = True
                                self.game.world = True
                                waiting = False
                                self.player.health = self.player.maxHealth
                                break
                                
                        elif self.menu.selected == 5:
                            escape = rd.randint(1, 5)
                            if escape >= 2: 
                                self.playing = False
                                self.game.player.completed_comp = True
                                self.game.world = True
                                self.player.health = self.player.maxHealth
                                waiting = False


                                break
                            else:
                                self.messagerLogger.logMessage("Failed to escape!")
                        
                    if event.key == py.K_p:
                        self.paused = not self.paused
                    
                    if self.menu.selected > len(self.menu.options) -1:
                        self.menu.selected = 5
                    if self.menu.selected < -1:
                        self.menu.selected = 0

    def decideturn(self):
        if self.opponent.speed > self.player.speed:
            self.playerFirst = False
        elif self.opponent.speed < self.player.speed:
            self.playerFirst = True
        else:
            choice = rd.randint(0,1)
            if choice == 1:
                self.playerFirst = True
            else:
                self.playerFirst = False

    def turn(self):
    
        if self.playerFirst:
            self.events()
        else:
            stillAlive = self.opponent.decideRandAttack(self.player, self.opponent)
            self.messagerLogger.logMessage(self.opponent.name + " used " + self.opponent.moves[self.menu.selected][0])
            self.messagerLogger.logMessage(self.player.name + "'s health decrease")
            if stillAlive == False:
                self.messagerLogger.logMessage(self.player.name + " is dead")
                self.game.player.completed_comp = True
                self.game.world = True
                self.player.health = self.player.maxHealth
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
                self.decideturn()
                self.draw()
                firstLoop = False
            
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
        self.draw_text((self.player.name + " - Gerald") , self.game.title_font, TEXTSIZE, BLACK, 325, 290, self.game.screen)
        self.draw_health_Bar(325, 338, int(self.player.health) / int(self.player.maxHealth))
        self.draw_text((self.opponent.name + " - Drake") , self.game.title_font, TEXTSIZE, BLACK, 255, 62, self.game.screen)
        self.draw_health_Bar(255, 100, int(self.opponent.health) / int(self.opponent.maxHealth))
        x = 50
        y = 450
        for message in self.messagerLogger.shownMessageList:
            self.draw_text(message, self.game.title_font, OTHERSIZE, BLACK, x, y, self.game.screen)
            y += 35
        self.opponent.draw(self.game.screen, 700, 50)
        self.player.draw(self.game.screen, 100, 200)
        py.display.flip()


    def update(self):
        py.display.set_caption("{:.2f}".format(self.game.clock.get_fps()))
        self.game.screen.blit(self.capture_background, (0, 0))
        self.sprites.update()