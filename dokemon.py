import pygame as py
import json
import os
import sys
import random as rd


with open("dokemon.json") as dokemon_file:
    data = json.load(dokemon_file)


class Dokemon(py.sprite.Sprite):
    def __init__(self, name, health, sp_defense, sp_attack, defense, speed, attack, attks, combat, game, img_file, powerlist):
        self.groups = combat.sprites
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = py.transform.scale(py.image.load(os.path.join(game.img_folder, img_file)).convert_alpha(), (150, 150))
        self.rect = self.image.get_rect()
        self.name = name
        self.health = health
        self.sp_defense = sp_defense
        self.sp_attack = sp_attack
        self.defense = defense
        self.speed = speed
        self.attack = attack
        self.maxHealth = health
        self.moves = attks
        self.power = powerlist

    def draw(self, surface, x, y):
        surface.blit(self.image, (x, y))


       
    def decideRandAttack(self, target):
        choice = rd.randint(0, 3)
        target.takeDamage(self,choice)
    def decideAttacks(self, choice, target):
        alive = target.takeDamage(self, choice)
        return alive
    def takeDamage(self, attacker, index):
        totalDm = (2/5 + 2 * attacker.power[index] * attacker.attack / self.defense) / 50 + 2
        print("Total damage:", totalDm)
        print("Total health:", self.health)
        self.health -= totalDm
        if self.health <= 0:
            return False
        else:
            return True
        
    

dokemonList = []