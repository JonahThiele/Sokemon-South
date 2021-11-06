import random as rd
class Dokemon:
    def __init__(self):
        self.attks = [["nice1", 10], ["nice2", 10], ["nice3", 10], ["nice4", 10]]
        self.health = 100
        self.maxHealth = 100
        self.speed = 0
        self.name = None
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
