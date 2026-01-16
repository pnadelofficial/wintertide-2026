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
        self.ability_uses = {}
        self.permanent_modifiers = {}

    def get_trait(self, trait_name):
        """Get current trait value including any modifiers"""
        return self.traits[trait_name]
    
    def modify_trait(self, trait_name, amount, permanent=False):
        """Modify a trait by a certain amount"""
        self.traits[trait_name] = max(0, self.traits[trait_name] + amount)
        if permanent:
            self.permanent_modifiers[trait_name] = self.permanent_modifiers.get(trait_name, 0) + amount
    
    def apply_incoming_damage(self, major_dmg, minor_dmg, opponent):
        """
        Hook for abilities that reduce incoming damage.
        Each character can override this method to implement their special ability.
        """
        return major_dmg, minor_dmg
    
    def pre_duel_effects(self, opponent):
        """
        Hook for abilities that trigger before duel calculations.
        Each character can override this method.
        """
        pass
    
    def post_duel_effects(self, opponent, major_dmg_dealt, minor_dmg_dealt):
        """
        Hook for abilities that trigger after dealing damage.
        Each character can override this method.
        """
        pass

class Parzival(Character):
    """For Herzeloyde! - Ignore minor trait damage 3 times"""
    def __init__(self):
        super().__init__(
            name="Parzival",
            honor=10,
            diplo=10,
            marti=20,
            stewa=9,
            intri=11,
            learn=5,
            special="For Herzeloyde!"
        )
        self.ability_uses["minor_ignore"] = 3
    
    def apply_incoming_damage(self, major_dmg, minor_dmg, opponent):
        if minor_dmg > 0 and self.ability_uses["minor_ignore"] > 0:
            print(f"  🛡️  {self.name} uses 'For Herzeloyde!' - ignores {minor_dmg} minor damage! ({self.ability_uses['minor_ignore']} uses remaining)")
            self.ability_uses["minor_ignore"] -= 1
            minor_dmg = 0
        return major_dmg, minor_dmg

class Gawan(Character):
    """Arm of Waleis - Ignore major trait damage once"""
    def __init__(self):
        super().__init__(
            name="Gawan",
            honor=10,
            diplo=14,
            marti=18,
            stewa=12,
            intri=11,
            learn=10,
            special="Arm of Waleis"
        )
        self.ability_uses["major_ignore"] = 1
    
    def apply_incoming_damage(self, major_dmg, minor_dmg, opponent):
        if major_dmg > 0 and self.ability_uses["major_ignore"] > 0:
            print(f"  🛡️  {self.name} uses 'Arm of Waleis!' - ignores {major_dmg} major damage!")
            self.ability_uses["major_ignore"] -= 1
            major_dmg = 0
        return major_dmg, minor_dmg

class Feirefiz(Character):
    """Sons of Gahmurat - Never take major damage from Parzival, gain stats when fighting him"""
    def __init__(self):
        super().__init__(
            name="Feirefiz",
            honor=10,
            diplo=9,
            marti=19,
            stewa=9,
            intri=8,
            learn=7,
            special="Sons of Gahmurat"
        )
    
    def apply_incoming_damage(self, major_dmg, minor_dmg, opponent):
        if opponent.name == "Parzival" and major_dmg > 0:
            print(f"  🛡️  {self.name} uses 'Sons of Gahmurat!' - brothers never harm each other! (ignores {major_dmg} major damage)")
            major_dmg = 0
        return major_dmg, minor_dmg
    
    def post_duel_effects(self, opponent, major_dmg_dealt, minor_dmg_dealt):
        if opponent.name == "Parzival":
            print(f"  ⚔️  {self.name}'s bond with his brother makes him stronger! (all non-Martial stats +1)")
            for trait in ["Diplomacy", "Stewardship", "Intrigue", "Learning"]:
                self.modify_trait(trait, 1, permanent=True)

class Cundrie(Character):
    """Oppressor of Joy - Decrease opponent stats by 2, three times"""
    def __init__(self):
        super().__init__(
            name="Cundrie la Surziere",
            honor=10,
            diplo=11,
            marti=9,
            stewa=15,
            intri=13,
            learn=18,
            special="Oppressor of Joy"
        )
        self.ability_uses["stat_decrease"] = 3
    
    def use_oppressor(self, opponent):
        """Manually trigger ability before a duel"""
        if self.ability_uses["stat_decrease"] > 0:
            print(f"  ✨ {self.name} uses 'Oppressor of Joy!' - {opponent.name}'s stats decreased by 2!")
            for trait in opponent.traits:
                opponent.modify_trait(trait, -2)
            self.ability_uses["stat_decrease"] -= 1
            return True
        else:
            print(f"  ❌ {self.name} has no uses of 'Oppressor of Joy' remaining!")
            return False

class Orgeluse(Character):
    """Haughty Maiden of Logres - Decrease opponent stats by 1, five times"""
    def __init__(self):
        super().__init__(
            name="Orgeluse",
            honor=10,
            diplo=16,
            marti=8,
            stewa=12,
            intri=17,
            learn=13,
            special="Haughty Maiden of Logres"
        )
        self.ability_uses["stat_decrease"] = 5
    
    def use_haughty_maiden(self, opponent):
        """Manually trigger ability before a duel"""
        if self.ability_uses["stat_decrease"] > 0:
            print(f"  ✨ {self.name} uses 'Haughty Maiden of Logres!' - {opponent.name}'s stats decreased by 1!")
            for trait in opponent.traits:
                opponent.modify_trait(trait, -1)
            self.ability_uses["stat_decrease"] -= 1
            return True
        else:
            print(f"  ❌ {self.name} has no uses of 'Haughty Maiden of Logres' remaining!")
            return False

class Arthur(Character):
    """The Round Table - Summon knights for one-time stat buffs with trade-offs"""
    def __init__(self):
        super().__init__(
            name="King Arthur",
            honor=10,
            diplo=15,
            marti=12,
            stewa=18,
            intri=9,
            learn=14,
            special="The Round Table"
        )
        self.ability_uses["knights"] = {
            "Kay": True,
            "Iwein": True,
            "Lanzelet": True
        }
    
    def summon_knight(self, knight_name):
        """Summon a knight from the Round Table for permanent stat changes"""
        if knight_name not in self.ability_uses["knights"]:
            print(f"  ❌ Unknown knight: {knight_name}")
            return False
        
        if not self.ability_uses["knights"][knight_name]:
            print(f"  ❌ Sir {knight_name} has already been summoned!")
            return False
        
        if knight_name == "Kay":
            print(f"  🗡️  {self.name} summons Sir Kay! (+3 Martial, -3 Stewardship)")
            self.modify_trait("Martial", 3, permanent=True)
            self.modify_trait("Stewardship", -3, permanent=True)
        elif knight_name == "Iwein":
            print(f"  💬 {self.name} summons Sir Iwein! (+3 Diplomacy, -3 Intrigue)")
            self.modify_trait("Diplomacy", 3, permanent=True)
            self.modify_trait("Intrigue", -3, permanent=True)
        elif knight_name == "Lanzelet":
            print(f"  🎭 {self.name} summons Sir Lanzelet! (+3 Intrigue, -3 Learning)")
            self.modify_trait("Intrigue", 3, permanent=True)
            self.modify_trait("Learning", -3, permanent=True)
        
        self.ability_uses["knights"][knight_name] = False
        return True

class Duel:
    def __init__(self, character1, major1, minor1, character2, major2, minor2):
        self.character1 = character1
        self.major1 = major1
        self.minor1 = minor1

        self.character2 = character2
        self.major2 = major2
        self.minor2 = minor2

        self.major1_num = self.character1.get_trait(self.major1)
        self.minor1_num = self.character1.get_trait(self.minor1)
        self.major2_num = self.character2.get_trait(self.major2)
        self.minor2_num = self.character2.get_trait(self.minor2)

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

    def play(self, verbose=True):
        """
        Play the duel and return damage dealt to each character.
        Returns: (char1_major_dmg, char1_minor_dmg, char2_major_dmg, char2_minor_dmg)
        """
        # Pre-duel effects
        self.character1.pre_duel_effects(self.character2)
        self.character2.pre_duel_effects(self.character1)
        
        major_res, major_winner, minor_res, minor_winner = self._subtract_and_find_balance()
        major_dmg = self._roll_die(major_res)
        minor_dmg = self._roll_die(minor_res)
        
        if verbose:
            print(f"\n⚔️  DUEL: {self.character1.name} vs {self.character2.name}")
            print(f"  {self.character1.name}: {self.major1}={self.major1_num}, {self.minor1}={self.minor1_num}")
            print(f"  {self.character2.name}: {self.major2}={self.major2_num}, {self.minor2}={self.minor2_num}")
        
        # major affinities
        if major_winner == self.character1:
            major_winning_trait = self.major1
            major_losing_trait = self.major2
            major_loser = self.character2
        else:
            major_winning_trait = self.major2
            major_losing_trait = self.major1
            major_loser = self.character1
            
        affinity_list = AFFINITIES[major_winning_trait]
        for affinity in affinity_list:
            post_affinity = affinity(major_losing_trait, major_dmg)
            if major_dmg != post_affinity:
                break
        major_dmg = post_affinity

        # minor affinities
        if minor_winner == self.character1:
            minor_winning_trait = self.minor1
            minor_losing_trait = self.minor2
            minor_loser = self.character2
        else:
            minor_winning_trait = self.minor2
            minor_losing_trait = self.minor1
            minor_loser = self.character1
            
        affinity_list = AFFINITIES[minor_winning_trait]
        for affinity in affinity_list:
            post_affinity = affinity(minor_losing_trait, minor_dmg)
            if minor_dmg != post_affinity:
                break
        minor_dmg = post_affinity
        minor_dmg = math.floor(minor_dmg/2)
        
        # Apply defensive abilities
        if major_loser == self.character1:
            char1_major_dmg, char1_minor_dmg = self.character1.apply_incoming_damage(major_dmg, 0, self.character2)
            char2_major_dmg, char2_minor_dmg = self.character2.apply_incoming_damage(0, minor_dmg, self.character1)
        else:
            char1_major_dmg, char1_minor_dmg = self.character1.apply_incoming_damage(0, minor_dmg, self.character2)
            char2_major_dmg, char2_minor_dmg = self.character2.apply_incoming_damage(major_dmg, 0, self.character1)
        
        # Apply damage to traits
        if char1_major_dmg > 0:
            if verbose:
                print(f"  💥 {self.character1.name} takes {char1_major_dmg} {major_losing_trait} damage!")
            self.character1.modify_trait(major_losing_trait, -char1_major_dmg)
            
        if char1_minor_dmg > 0:
            if verbose:
                print(f"  💥 {self.character1.name} takes {char1_minor_dmg} {minor_losing_trait} damage!")
            self.character1.modify_trait(minor_losing_trait, -char1_minor_dmg)
            
        if char2_major_dmg > 0:
            if verbose:
                print(f"  💥 {self.character2.name} takes {char2_major_dmg} {major_losing_trait} damage!")
            self.character2.modify_trait(major_losing_trait, -char2_major_dmg)
            
        if char2_minor_dmg > 0:
            if verbose:
                print(f"  💥 {self.character2.name} takes {char2_minor_dmg} {minor_losing_trait} damage!")
            self.character2.modify_trait(minor_losing_trait, -char2_minor_dmg)
        
        total_char2_dmg = char2_major_dmg + char2_minor_dmg
        if total_char2_dmg > 0:
            self.character2.honor = max(0, self.character2.honor - total_char2_dmg)
            if verbose:
                print(f"  ❤️  {self.character2.name}'s honor reduced by {total_char2_dmg}!")

        # Post-duel effects
        if major_winner == self.character1:
            self.character1.post_duel_effects(self.character2, major_dmg, 0)
            self.character2.post_duel_effects(self.character1, 0, minor_dmg)
        else:
            self.character1.post_duel_effects(self.character2, 0, minor_dmg)
            self.character2.post_duel_effects(self.character1, major_dmg, 0)
        
        return char1_major_dmg, char1_minor_dmg, char2_major_dmg, char2_minor_dmg

parzival = Parzival()
gawan = Gawan()
feirefiz = Feirefiz()
cundrie = Cundrie()
orgeluse = Orgeluse()
arthur = Arthur()