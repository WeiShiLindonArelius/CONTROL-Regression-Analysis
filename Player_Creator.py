from Players import Player
from random import randint, choice, uniform
names = [
  "Aria", "Ashton", "Amara", "Ari", "Anya",
  "Bryce", "Brennan", "Briar", "Brodie",
  "Calla", "Cameron", "Carson", "Cassius", "Chase",
  "Dakota", "Darcy", "Dallas", "Darian", "Devin",
  "Ellis", "Elliott", "Emery", "Eris", "Evelyn",
  "Finley", "Flynn", "Finnegan", "Felicity", "Freya",
  "Gia", "Gael", "Gwen", "Gunnar", "Giselle",
  "Harlow", "Harper", "Hayden", "Hadley", "Hunter",
  "Iris", "Indiana", "Isadora", "Isla", "Imogen",
  "Jude", "Jordan", "Jax", "Jasper", "Jocelyn",
  "Kai", "Carter", "Keegan", "Kendall", "Kyra",
  "Lennon", "Linden", "Landon", "Logan", "Lorelei",
  "Madden", "Marley", "Maddox", "Mason", "Mila",
  "Nova", "Nash", "Nico", "Nolan", "Naya",
  "Oakley", "Odessa", "Orion", "Oliver", "Ophelia",
  "Parker", "Phoenix", "Presley", "Paxton", "Primrose",
  "Quinn", "Quincy", "Quest", "Queenie", "Quinten",
  "Rowan", "Reagan", "Reeve", "Raven", "Ryder",
  "Sage", "Sawyer", "Saylor", "Sutton", "Sparrow",
  "Tatum", "Tanner", "Tate", "Theo", "Tilly",
  "Urban", "Uriel", "Ulysses", "Umberto", "Una",
  "Vesper", "Vida", "Valentine", "Vance", "Verity",
  "Wren", "Weston", "Willow", "Wilder", "Winslow",
  "Xanthe", "Xander", "Ximena", "Xiomara", "Xena",
  "Yara", "Yasmine", "Yael", "Yvette", "Yvonne",
  "Zephyr", "Zara", "Zander", "Zeke", "Zelda", "Zain",
    "Killer", "Zoro", "Luffy", "Brook", "Nami"
]

def apply_traits(player):
    #todo implement function in game() to allow for player traits

    #every time a player is created, they are run through this function at the end.
    #they have a certain chance, depending on their tier, to gain each trait
    #if they fail to gain a trait, the function passes. if they gain a trait, it applies the tag and the necessary
    #statistic modifications
    #possible traits: ''Nuclear', 'Healer', 'Clutch, 'Butler, or 'Reflector'
    #each tier has a chance to gain a trait (calculated by uniform(0,1)), and for each player which gets a trait, they are assigned one via choice()
    chance_dict = {'S' : uniform(0.03,0.05), 'A' : uniform(0.025,0.055), 'B' : uniform(0.02,0.06), 'C' : uniform(0.015,0.075)}
    coin = uniform(0,1)
    if coin < chance_dict[player.tier]:
        to_apply = choice(['Nuclear', 'Healer', 'Clutch', 'Butler', 'Reflector'])
        player.trait_tag = to_apply #the main functions of the majority of traits will happen on runtime in lineup() in Game.py
        #based on the trait tag applied here
        #beyond this, this only serves to make the baseline statistical modifications that apply only to Nuclear and Reflector
        if to_apply == 'Nuclear':
            player.health = round(player.health*0.75, 2)
            player.atk_dmg = round(player.atk_dmg*0.75)
        if to_apply == 'Reflector':
            player.crit_x = round(player.crit_x*0.5, 2)




def s_tier(amp=0):
    # Generate random integer values for each stat within the specified range for S tier
    atk_dmg = randint(45, 60)
    atk_spd = randint(6, 14)
    crit_pct = round((((randint(25, 55)) / 1000) + (amp * 0.01)),2)
    crit_x = round(((randint(800, 1200)/100) + (amp * 0.1)), 2)
    health = round(uniform(525,575),2)
    power = randint(52, 59)
    spawn_time = randint(10, 14)
    crit_dmg = atk_dmg*crit_x
    # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("S", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, f"S_{choice(names)}")
    else:
        return Player(f"S", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"S^{amp}_{choice(names)}")

def a_tier(amp=0):
    # Generate random integer values for each stat within the specified range for A tier
    atk_dmg = randint(45, 60) + int(amp*0.75)
    atk_spd = randint(7, 15) + int(amp*0.3)
    crit_pct = (randint(20, 45))/1000
    crit_x = randint(700, 1100)/100
    health = round(uniform(500,565),2) + round((25*amp),2)
    power = randint(51, 59) + int(amp*0.25)
    spawn_time = randint(10, 14)
    crit_dmg = atk_dmg * crit_x
    # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("A", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"A_{choice(names)}")
    else:
        return Player(f"A", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"A^{amp}_{choice(names)}")

def b_tier(amp=0):
    # Generate random integer values for each stat within the specified range for B tier
    atk_dmg = randint(40, 55) + int(amp*1.5)
    atk_spd = randint(8, 15) - int(amp/2)
    crit_pct = (randint(21,46))/1000
    crit_x = randint(500, 900)/100
    health = round(uniform(495,555),2)
    power = randint(50, 58)
    spawn_time = randint(11, 14) - int(amp/3)
    crit_dmg = atk_dmg * crit_x
    # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("B", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"B_{choice(names)}")
    else:
        return Player(f"B", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"B^{amp}_{choice(names)}")

def c_tier(amp=0):
    atk_dmg = randint(30, 52)
    atk_spd = randint(9, 16)
    crit_pct = round((((randint(20, 50)) / 1000) + (amp * 0.01)),2)
    crit_x = randint(1175, 1350)/100 + float(amp/10)
    health = round(uniform(525,575),2)
    power = randint(49, 57)
    spawn_time = randint(11, 15)
    crit_dmg = atk_dmg * crit_x
            # Return a Player object initialized with the generated values
    if amp == 0:
        return Player("C", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, f"C_{choice(names)}")
    else:
        return Player("C", atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                      f"C^{amp}_{choice(names)}")