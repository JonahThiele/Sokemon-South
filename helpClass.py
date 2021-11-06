import pygame as py
import sys

py.init()

white = (255, 255, 255)

class Help():

    def runHelp(self):
        screen = py.display.set_mode(size = (500, 500))
        py.display.set_caption("Help Screen")
        screen.fill(white)
        py.display.update()
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    py.quit()
                    sys.exit()
