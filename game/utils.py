import math
import random

class Character:
    def __init__(self, name, honor, diplo, marti, stewa, intri, learn):
        self.name = name
        self.honor = honor
        self.traits = {"Diplomacy":diplo, "Martial":marti, "Stewardship":stewa, "Intrigue":intri, "Learning":learn}

class Duel:
    def __init__(self, character1, major1, minor1, character2, major2, minor2):
        self.character1 = character1
        self.major1 = major1
        self.minor1 = minor1

        self.character2 = character2
        self.major2 = major2
        self.minor2 = minor2

        self.major1_num = self.character1[self.major1]
        self.minor1_num = self.character1[self.minor1]
        self.major2_num = self.character2[self.major2]
        self.minor2_num = self.character2[self.minor2]

    def _subtract_and_find_balance(self):
        # major 
        major_res = self.major_num1 - self.major_num2
        if major_res > 0:
            major_winner = self.character1
        else:
            major_winner = self.character2
        
        # minor
        minor_res = self.minor_num1 - self.minor_num2
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

