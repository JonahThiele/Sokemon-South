import pygame as py
import json

with open("dokemon.json") as dokemon_file:
    data = json.load(dokemon_file)





class Dokemon:
    def __init__(self, name, health, sp_defense, sp_attack, defense, speed):
        self.name = name
        self.health = health
        self.sp_defense = sp_defense
        self.sp_attack = sp_attack
        self.defense = defense
        self.speed = speed
        
    

dokemonList = []

for dokemon in data['possibleDokemon']:
    name = str(dokemon['name'])
    for stats in dokemon['stats']:
        health = stats['health']
        defense = stats['defense']
        speed = stats['speed']
        sp_attack = stats['sp. attack']
        sp_defense = stats['sp. defense']
        
        new = Dokemon(name, health, sp_defense, sp_attack, defense, speed)
    dokemonList.append(new)
    
for dokemon in dokemonList:
    print(dokemon.sp_attack)