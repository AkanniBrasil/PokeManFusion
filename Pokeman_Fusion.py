#Proposed challenge: Make a simple turn based game in the style of pokemon, using OOP to create the characters both PC and Player can use, while also adding a layer of complexity with the ability to fuse said characters.



import copy
import random


#Super effectiveness dictionary
beats = {"fire":"water",
    "grass":"fire",
    "rock":"grass",
    "electro":"rock",
    "man":"electro",
    "water":"man",
    "normal":"normal"}

class man():
    def __init__(self, name=' ', type=() , _health=0, attack=0 ):
        self.name = name
        self.type = type
        self._health = _health
        self.attack = attack
    
        #attack method
    def attack_enemy(self,other):
        print(f"\n{self.name} is attacking {other.name}!")
        effective = False
        
       # Flatten both self.type and other.type into tuples
        attacker_types = (self.type,) if isinstance(self.type, str) else self.type
        defender_types = (other.type,) if isinstance(other.type, str) else other.type

        #Check if any of attacker's types beat any of defender's types
        for atk_type in attacker_types:
            for def_type in defender_types:
                if beats.get(def_type) == atk_type:
                    effective = True
                    break  
            if effective:
                break  
        if effective:
            print(f"\n{self.name} attacks with the power of {self.type}! It's a MANLY attack!")
            damage = self.attack * 2
        else:
            print("\nAn unimpressive attack!")
            damage = self.attack
        
        other._health -= damage
        other._health = max(other._health,0)
        print(f"{self.name} deals {damage} damage!")

    def health_inspect(self):
        print(f"{self.name} has {self._health} HP left!")

    #Inspect function that returns the current character type, it's super effective strength and current HP
    def full_inspect(self):
        if isinstance(self.type,tuple):
            strong_against = set()
            for t in self.type:
                strong_against.update([key for key, value in beats.items() if value == t]) 
            if strong_against:
                print(f"\n{self.name} is strong against the {str(' and '.join(strong_against))} types!")
        else:
            strong_against = [key for key, value in beats.items() if value == self.type]
            if strong_against:
                print(f"\n{self.name} is of the {self.type} type. It is strong against the {str(strong_against)} type") 
        print(f"{self.name} has {self._health} HP left!\n")
        
    

#choices both users will have. added normal type so it is a tuple
waterman = man(name='waterman',type=('water'), _health=50, attack=10)
fireman = man(name='fireman',type=('fire'),_health=50, attack=10)
grassman = man(name='grassman', type =('grass'), _health=50, attack=10)
rockman = man(name='rockman', type=('rock'), _health=50, attack=10)
electroman = man(name='electroman',type=('electro'), _health=50, attack=10)
manman = man(name='manman', type=('man'), _health=50, attack=10)

#compiling the lists of men for player and computer to use
man_list = [waterman, fireman, grassman, rockman, electroman, manman]

man_list_com = copy.deepcopy(man_list)


def com_play():
    com_choice = random.choice(man_list_com)
    return com_choice


def player_choice():
    while True:
        try:
            print("\nCHOOSE YOUR MAN! YOU HAVE:")
            for man in man_list:
                man.name = str.capitalize(man.name)
                print(f"\n ◆ {man.name.ljust(10)} | HP: {man._health}")
    
            print ("\n")
            player = str(input())
            player = player.lower()
            if player in [man.name.lower() for man in man_list]:
                return player
            else:
                print("\n\nInvalid Man! Pick one of the following:")
        except ValueError:
            print("\n\nInvalid Input. Please pick one of the following options:")
    

def get_player_choice():
    #The player choice is defined and played
    player_choice_name = player_choice()
    player_choice_man = next(man for man in man_list if man.name.lower() == player_choice_name.lower())
    if player_choice_man:
        return player_choice_man
    else:
        print("Invalid Man! Please pick a valid option!")
    

#Here is the function for when the player picks the option to fuse and creates the new fusion man
def get_fusion_choice():
    while True:
        try:
            fusion_1_name = player_choice()	
            fusion_1_man = next(man for man in man_list if man.name.lower() == fusion_1_name.lower())
            if fusion_1_man:
                man_list.remove(fusion_1_man)
                print("SELECT THE OTHER MAN")
                fusion_2_name = player_choice()
                fusion_2_man = next(man for man in man_list if man.name.lower() == fusion_2_name.lower())
                if fusion_2_man:
                    man_list.remove(fusion_2_man)
                    fusion_types = () 
                    if isinstance(fusion_1_man.type, tuple):
                        fusion_types += fusion_1_man.type
                    else:
                        fusion_types += (fusion_1_man.type,)
                    if isinstance(fusion_2_man.type, tuple):
                        fusion_types += fusion_2_man.type
                    else:
                        fusion_types += (fusion_2_man.type,)
                    fusion_health = fusion_1_man._health + fusion_2_man._health
                    fusion_attack = fusion_1_man.attack + fusion_2_man.attack
                    megaman = man(name='THE MEGAMAN', type=fusion_types, _health= fusion_health, attack= fusion_attack)
                    man_list.append(megaman)
                    print(f"\n Fusion complete! Meet the {megaman.name}, a Man with types {megaman.type}")
                    return megaman
            else:
                 print("Invalid Man! Please pick a valid option!")
                
                
        except ValueError:
            print("Invalid Option! Please pick a valid option.")				

def action(player_choice_man, com_choice):
     
    while True:
        try:
            action = str(input("ATTACK, CHANGE, INSPECT or FUSION:  "))
            action = action.lower()
            if action == "attack":
                player_choice_man.attack_enemy(com_choice)
                return player_choice_man #return same player choice if attacking	
            elif action == "change":
                player_choice_man = get_player_choice()
                player_choice_man.name = str.capitalize(player_choice_man.name)
                print(f"You chose {player_choice_man.name}!")
                return player_choice_man #return new player choice		
            elif action == "fusion":
                player_choice_man = get_fusion_choice()
                player_choice_man.name = str.capitalize(player_choice_man.name)
                return player_choice_man
            elif action == "inspect":
                player_choice_man.full_inspect()
                pass
            else:
                print("Invalid action. Please pick one of the options above!")
        except ValueError:
            print("Invalid Input. Please type one of the options above.")
                            
def play_game():
    rounds = 0
    while True:
        #player turn
        player_choice_man = get_player_choice()
        player_choice_man.name = str.capitalize(player_choice_man.name)
            
    #Computer choice is defines and played
        com_choice = com_play()
        com_choice.name = str.capitalize(com_choice.name)
        print(f"\nYou chose {player_choice_man.name}! Enemy chose EVIL {com_choice.name}!")
        
        #Combat phase
        while player_choice_man._health > 0 and com_choice._health > 0:
                #players turn
            print(f"\nWhat will {player_choice_man.name} do?")
            player_choice_man = action(player_choice_man, com_choice) #pass player and computer choice to action function
            
            #Check if computer man is defeated
            if com_choice._health <= 0:
                print("**********************************************")
                print(f"{com_choice.name} suffered a humiliating defeat!")
                man_list_com.remove(com_choice)
                if man_list_com:
                    com_choice = com_play()
                    print(f"\nIt seems your enemy is not out of options!)\n\nEnemy chose EVIL {com_choice.name}!")
                    print("**********************************************")
                else:
                    print("CONGRATULATIONS! It seems you are a REAL MAN HANDLER! You win!")
                    return #Exit the function if the computer has no more men
                
        
        #computers turn
            com_choice.attack_enemy(player_choice_man)
        

            #Print HP remaining each round and current round
            rounds += 1
            print(f"\n ROUND {rounds} RESULTS:")
            player_choice_man.health_inspect()
            com_choice.health_inspect()
                
        #Check if player's man is defeated
            if player_choice_man._health <= 0:
                print(f"{player_choice_man.name} suffered a humiliating defeat!")
                man_list.remove(player_choice_man)
                break	


        #check if game is over
            
        if not man_list:
            print("Seems like you CAN'T HANDLE REAL MEN. YOU LOSE!!!!!")
            return #exit when the player has no men left

        

                
if __name__ == "__main__":
    print(" _    _  _____  _      _____  _____ ___  ___ _____   _____  _____   ______  _____  _   __ _____ ___  ___  ___   _   _ ")
    print("| |  | ||  ___|| |    /  __ \|  _  ||  \/  ||  ___| |_   _||  _  |  | ___ \|  _  || | / /|  ___||  \/  | / _ \ | \ | |")
    print("| |  | || |__  | |    | /  \/| | | || .  . || |__     | |  | | | |  | |_/ /| | | || |/ / | |__  | .  . |/ /_\ \|  \| |")
    print("| |/\| ||  __| | |    | |    | | | || |\/| ||  __|    | |  | | | |  |  __/ | | | ||    \ |  __| | |\/| ||  _  || . ` |")
    print("\  /\  /| |___ | |____| "" \__/\\ \_/ /| |  | || |___    | |  \ \_/ /  | |    \ \_/ /| |\  \| |___ | |  | || | | || |\  |")
    print(" \/  \/ \____/ \_____/ \____/ \___/ \_|  |_/\____/    \_/   \___/   \_|     \___/ \_| \_/\____/ \_|  |_/\_| |_/\_| \_/")
       
    text = "A game where your MEN will fight other MEN!\n\nMen have types and take double damage from their weaknessess!\n\nDouble damage goes: Water > Fire > Grass > Rock > Electro > Man > Water"
    line = "*" * (len(text)- 62)
    print(line)
    print(text)
    print(line)
    play_game()
                