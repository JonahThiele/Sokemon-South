import pygame as py
import json
import os
import sys
import random as rd


with open("dokemon.json") as dokemon_file:
    data = json.load(dokemon_file)


class Dokemon(py.sprite.Sprite):
    def __init__(self, name, health, sp_defense, sp_attack, defense, speed, attack, attks, combat, game, img_file):
        self.groups = combat.sprites
        py.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = py.image.load(os.path.join(game.img_folder, img_file)).convert_alpha()
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

    
    def moveSet(self):
        for dokemon in data['possibleDokemon']:
            if self.name == dokemon['name']:
                for possibleMove in dokemon['moves']:
                    move = possibleMove['moveName']
                    self.attks.append(move)

       
    def decideRandAttack(self, target):
        choice = rd.choice(self.moves)
        target.takeDamage(choice[1])
    def decideAttacks(self, choice, target):
        alive = target.takeDamage(self.moves[choice][1])
        return alive
    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return False
        else:
            return True
        
    

dokemonList = []