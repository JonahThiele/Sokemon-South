import pygame as py
import sys
import random
from buttonClass import *
from helpClass import *

game_names = ["Pokemon Powellite", "Pokemon Special", "Nintendo please don't send us a cease and desist!", "gay Bois"]

# Color Variables
white = (255, 255, 255)

py.init()



class Game():        

    def runHome(self):
        screen = py.display.set_mode(size = (500, 500))
        py.display.set_caption(random.choice(game_names))
        width = screen.get_width()
        height = screen.get_height()
        screen.fill(white)
        playButton = Button(width/4, height/2, 250, 50, 'Play')
        playButton.draw(screen, outline=None)
        helpButton = Button(width/4, height*.7, 250, 50, 'Help')
        helpButton.draw(screen, outline=None)
        title = Title((0,0,0), width/4, height*.2, 250, 50, 'Sokemon South')
        title.draw(screen, outline=False)
        py.display.update()
        while (True):
            
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        sys.exit()
                if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = py.mouse.get_pos()
                    if playButton.isOver(mouse):
                        py.quit()
                        sys.exit()
                    if helpButton.isOver(mouse):
    
                        help = Help()

                        help.runHelp()