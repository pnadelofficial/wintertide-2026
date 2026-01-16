import math
import random

AFFINITIES = {
    "Diplomacy": [lambda x,h: h*2 if x == "Stewardship" else h, lambda x,h: 0 if x == "Intrigue" else h],
    "Martial": [lambda x,h: math.floor(h*1.5) if x == "Learning" else h, lambda x,h: math.floor(h*.5) if x == "Intrigue" else h],
    "Stewardship": [lambda x,h: h*2 if x == "Intrigue" else h, lambda x,h: 0 if x == "Learning" else h],
    "Intrigue": [lambda x,h: h*2 if x == "Diplomacy" else h, lambda x,h: math.floor(h*.5) if x == "Learning" else h],
    "Learning": [lambda x,h: h*2 if x == "Stewardship" else h, lambda x,h: 0 if x == "Martial" else h]
}

class Character:
    def __init__(self, name, honor, diplo, marti, stewa, intri, learn, special):
        self.name = name
        self.honor = honor
        self.traits = {"Diplomacy":diplo, "Martial":marti, "Stewardship":stewa, "Intrigue":intri, "Learning":learn}
        self.special = special

class Duel:
    def __init__(self, character1, major1, minor1, character2, major2, minor2):
        self.character1 = character1
        self.major1 = major1
        self.minor1 = minor1

        self.character2 = character2
        self.major2 = major2
        self.minor2 = minor2

        self.major1_num = self.character1.traits[self.major1]
        self.minor1_num = self.character1.traits[self.minor1]
        self.major2_num = self.character2.traits[self.major2]
        self.minor2_num = self.character2.traits[self.minor2]

    def _subtract_and_find_balance(self):
        # major 
        major_res = self.major1_num - self.major2_num
        if major_res > 0:
            major_winner = self.character1
        else:
            major_winner = self.character2
        
        # minor
        minor_res = self.minor1_num - self.minor2_num
        if minor_res > 0:
            minor_winner = self.character1
        else:
            minor_winner = self.character2
        
        return abs(major_res), major_winner, math.floor(abs(minor_res)), minor_winner

    def _roll_die(self, res):
        roll = random.randint(1, res+1)
        return roll

    def play(self):
        major_res, major_winner, minor_res, minor_winner = self._subtract_and_find_balance()
        major_dmg = self._roll_die(major_res)
        minor_dmg = self._roll_die(minor_res)
        
        # major affinities
        if major_winner == self.character1:
            major_winning_trait = self.major1
            major_losing_trait = self.major2
        else
:
            major_winning_trait = self.major2
            major_losing_trait = self.major1
        affinity_list = AFFINITIES[major_winning_trait](major_losing_trait, major_dmg)

        
        
        return major_dmg, math.floor(minor_dmg/2)

