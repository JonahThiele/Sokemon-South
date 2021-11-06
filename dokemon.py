import pygame as py
import json
import random as rd

with open("dokemon.json") as dokemon_file:
    data = json.load(dokemon_file)





class Dokemon:
    def __init__(self, name, health, sp_defense, sp_attack, defense, speed, attack):
        self.name = name
        self.health = health
        self.sp_defense = sp_defense
        self.sp_attack = sp_attack
        self.defense = defense
        self.speed = speed
        self.attack = attack
    
    def moveSet(self):
        for dokemon in data['possibleDokemon']:
            if self.name == dokemon['name']:
                for possibleMove in dokemon['moves']:
                    move = possibleMove['moveName']
                    self.attks.append(move)

       
    def decideRandAttack(self, target):
        choice = rd.choice(self.attks)
        target.takeDamage(choice[1])
    def decideAttacks(self, choice, target):
        alive = target.takeDamage(self.attks[choice][1])
        return alive
    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return False
        else:
            return True
        
    

dokemonList = []

for dokemon in data['possibleDokemon']:
    name = str(dokemon['name'])
    for stats in dokemon['stats']:
        health = stats['health']
        defense = stats['defense']
        speed = stats['speed']
        sp_attack = stats['sp. attack']
        sp_defense = stats['sp. defense']
        attack = stats['attack']
        new = Dokemon(name, health, sp_defense, sp_attack, defense, speed, attack)
    dokemonList.append(new)