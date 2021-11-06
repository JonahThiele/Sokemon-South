from settings import *
import pygame as py

class Combat:
    def __init__(self, game):
        #class declare for wild dokemon
        self.wild_dokemon = None
        self.capture_background = game.combatBackground
        self.paused = False

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

    def initialize(self):
        self.sprites = py.sprite.Group()
        self.draw_text("Combat initialized", self.game.title_font, 20, BLACK, WIDTH / 2, HEIGHT - 10, self.game.screen)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
    
    def update(self):
        self.sprites.update()
        py.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.capture_background, (0, 0))
            
