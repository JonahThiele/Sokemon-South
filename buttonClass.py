import pygame as py
import random

gold = (255, 223, 0)
blue = (0, 0, 255)
colors = [gold, blue]

class Button():

    def __init__(self, x, y, width, height, text=''):
        self.color = random.choice(colors)
        colors.remove(self.color)

        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = py.Surface([self.width, self.height])
        self.Rect = self.image.get_rect()
        self.text = text
        

    def draw(self, win, outline=None):
        if outline:
            py.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        py.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = py.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if self.Rect.collidepoint(pos):
            return True
        return False
        


class Title():

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self, win, outline=None):
        if self.text != '':
            font = py.font.SysFont('comicsans', 45)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
