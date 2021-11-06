import pygame as py

py.init()

# Color Variables

white = (255, 255, 255)

def homeScreen():
    screen = py.display.set_mode(size = (500, 500))
    py.display.set_caption("Sokemon South")
    width = screen.get_width()
    height = screen.get_height()
    screen.fill(white)
    py.display.update()