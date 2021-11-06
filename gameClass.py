import pygame as py
import sys
from homeScreenFunction import homeScreen

class Game():


    def run(self):
        homeScreen()
        while (True):
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        sys.exit()