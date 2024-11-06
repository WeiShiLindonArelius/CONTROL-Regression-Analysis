from Players import Player
from random import randint, choice, uniform
import numpy as np
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

#If the reflector trait doesn't hit, this will trigger next.
#This returns "" if the player is not given a trait, and the trait tag along with a multiplier if they are
def additional_trait_roll(tier, fixed="None",amp=0,pre_reflect=0):
    #amp is no longer being used because of mathematical issues
    clutch_lower_bound = 1.05
    inc_lower_bound = 0.05
    pp_lower_bound = 0.2
    if tier == 'S':
        clutch_upperbound = 1.2
        inc_upperbound = 0.1
        pp_upperbound = 0.4
    elif tier == 'A':
        clutch_upperbound = 1.25
        inc_upperbound = 0.095
        pp_upperbound = 0.45
    elif tier == 'B':
        clutch_upperbound = 1.275
        inc_upperbound = 0.09
        pp_upperbound = 0.5
    elif tier == 'C':
        clutch_upperbound = 1.2875
        inc_upperbound = 0.085
        pp_upperbound = 0.6
    elif tier == 'U-' or tier == '$l':
        return ["None",0]
    else:
        #Error handling block; this should never happen
        clutch_upperbound = 1.3
        inc_upperbound = 0.1
        pp_upperbound = 0.14


    if fixed == 'C%':
        return ['C%', round(uniform(clutch_lower_bound,clutch_upperbound),2)]
    elif fixed == 'I*':
        return ['I*', round(uniform(inc_lower_bound,inc_upperbound),2)]
    elif fixed == 'Pp':
        return ['Pp', round(uniform(pp_lower_bound,pp_upperbound),2)]
    else:
        trait_roll = randint(0,100) / 100
        # Clutch 5% // Inconsistent 7.5% // Playoff Performer 5% // Reflector 7.5%
        #
        # Total: 25% chance of trait
        if pre_reflect == 1:
            #positive values below 1 should do nothing now that reflector is a normal trait and not separate from the others
            return ['R#', 0]
        elif np.logical_and(0 <= trait_roll, trait_roll <= 0.05):
            return ['C%', round(uniform(clutch_lower_bound,clutch_upperbound),2)]
        elif np.logical_and(0.05 < trait_roll, trait_roll <= 0.125):
            return ['I*', round(uniform(inc_lower_bound,inc_upperbound),2)]
        elif np.logical_and(0.125 < trait_roll, trait_roll <= 0.175):
            return ['Pp', round(uniform(pp_lower_bound,pp_upperbound),2)]
        elif np.logical_and(0.175 < trait_roll, trait_roll <= 0.25):
            return ['R#', 0]
            #reflectors do not have a multiplier
        else:
            return ["None",0]



def undead(amp=0, season_count=-1):
    #in the game function, if trait_tag='U-' it rolls the dice for revival
    atk_dmg = randint(40,55)
    atk_spd = randint(7, 14)
    crit_pct = (randint(23,49))/1000
    crit_x = randint(450, 850)/100
    health = round(uniform(435,505),2)
    power = randint(49, 58) #avg 53.5 (5th of 6)
    spawn_time = randint(10, 15)
    crit_dmg = atk_dmg*crit_x

    undead_chance = choice([0.29,0.29,0.3,0.3,0.3,0.3,0.31,0.32,0.33]) + (round((0.075*amp), 2))

    amp_str = "" if amp==0 else f"^{amp}"
    return Player('$', atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, f"U-{amp_str}_{choice(names)}",amp=amp, season_count=season_count, undead_chance=undead_chance, trait_tag="U-")


def slasher(amp=0, season_count=-1):
    #SLASHER
    #Special Trait: all critical hits deal damage equal to the maximum health of the player they are attacking
    #Stat Pros: Very high attack damage, fast attack speed
    #Stat Cons: Very low health, very low power, high spawn time
    #Tag: '$'

    atk_dmg = randint(55, 70) + round(amp*2)
    atk_spd = randint(6, 9)
    insta_kill_pct = round((((randint(42, 58)) / 1000) + (amp * 0.0095)),2)
    crit_pct = insta_kill_pct
    crit_x = round((700 / atk_dmg), 2) #700 is just above average health; finds crit_x backwards from instant kill for xWAR purposes
    health = choice([round(uniform(450, 550), 2), round(uniform(425, 575), 2)])
    power = choice([randint(48, 55), randint(50, 54)]) #avg 51.75 (6th of 6)
    spawn_time = choice([11,11,12,13,14])
    crit_dmg = atk_dmg * crit_x

    amp_str = "" if amp==0 else f"^{amp}"
    return Player('$l', atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, f"$l{amp_str}_{choice(names)}",amp=amp, season_count=season_count, insta_kill_pct=insta_kill_pct, trait_tag="$l")

def s_tier(amp=0, season_count=-1, pre_reflect=0, trait_amp=0, fixed='None'):
    atk_dmg = randint(45, 60)
    atk_spd = randint(6, 14)
    crit_pct = round((((randint(25, 55)) / 1000) + (amp * 0.01)),2)
    crit_x = round(((randint(800, 1200)/100) + (amp * 0.1)), 2)
    health = round(uniform(525,575),2)
    power = randint(52, 59) #avg 55.5
    spawn_time = randint(10, 14)
    crit_dmg = atk_dmg*crit_x
    # Return a Player object initialized with the generated values

    amp_str = "" if amp == 0 else f"^{amp}"
    tag, mult = additional_trait_roll('S',amp=trait_amp,pre_reflect=pre_reflect, fixed=fixed)
    return Player('S', atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                  f"S{amp_str}_{choice(names)}", amp=amp, season_count=season_count,
                  trait_tag=tag, trait_multiplier=mult)




def a_tier(amp=0, season_count=-1, pre_reflect=0, trait_amp=0, fixed='None'):
    atk_dmg = randint(45, 60) + int(amp*0.75)
    atk_spd = randint(7, 15)
    crit_pct = (randint(20, 45))/1000
    crit_x = randint(700, 1100)/100
    health = round(uniform(500,565),2) + round((25*amp),2)
    power = randint(51, 59) #avg 55
    spawn_time = randint(10, 14)
    crit_dmg = atk_dmg * crit_x
    # Return a Player object initialized with the generated values
    amp_str = "" if amp == 0 else f"^{amp}"
    tag, mult = additional_trait_roll('A',amp=trait_amp,pre_reflect=pre_reflect, fixed=fixed)
    return Player('A', atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                  f"A{amp_str}_{choice(names)}", amp=amp, season_count=season_count,
                  trait_tag=tag, trait_multiplier=mult)


def b_tier(amp=0, season_count=-1, pre_reflect=0, trait_amp=0, fixed='None'):
    atk_dmg = randint(40, 55) + int(amp*1.5)
    atk_spd = randint(8, 15) - int(amp/2)
    crit_pct = (randint(21,46))/1000
    crit_x = randint(500, 900)/100
    health = round(uniform(495,555),2)
    power = randint(50, 58) #avg 54
    spawn_time = randint(11, 14) - int(amp/3)
    crit_dmg = atk_dmg * crit_x
    # Return a Player object initialized with the generated values
    amp_str = "" if amp == 0 else f"^{amp}"
    tag, mult = additional_trait_roll('B',amp=trait_amp,pre_reflect=pre_reflect, fixed=fixed)
    return Player('B', atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                  f"B{amp_str}_{choice(names)}", amp=amp, season_count=season_count,
                  trait_tag=tag, trait_multiplier=mult)

def c_tier(amp=0, season_count=-1, pre_reflect=0, trait_amp=0, fixed='None'):
    atk_dmg = randint(30, 52)
    atk_spd = randint(9, 14)
    crit_pct = round((((randint(20, 50)) / 1000) + (amp * 0.01)),2)
    crit_x = randint(1175, 1350)/100 + float(amp/10)
    health = round(uniform(525,575),2)
    power = randint(49, 57) #avg 53
    spawn_time = randint(11, 15)
    crit_dmg = atk_dmg * crit_x
            # Return a Player object initialized with the generated values
    amp_str = "" if amp == 0 else f"^{amp}"
    tag, mult = additional_trait_roll('C',amp=trait_amp,pre_reflect=pre_reflect, fixed=fixed)
    return Player('C', atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg,
                  f"C{amp_str}_{choice(names)}", amp=amp, season_count=season_count,
                  trait_tag=tag, trait_multiplier=mult)
