from random import choice, seed, uniform
from Player_Creator import s_tier, a_tier, b_tier, c_tier
from colorama import Fore, Back, Style
from numpy import mean

import itertools

def grade_players(players, is_team=None):
    #should take in a list of players, not a dict draft class

    pos_xWAR_coefficient = {'1 Attack Speed' : -61.46, '1 Attack Damage' : 16.67, '1 Health' : 0.34,
                            '1 Power' : 283.01, '1 Spawn Time' : -149.98, '.001 Critical Chance' : 26.40,
                            '.1 Critical Multiplier' : 0.79}
    #positive coefficient is multiplied by (player_stat - average_stat) if player_stat > average_stat

    neg_xWAR_coefficient = {'1 Attack Speed' : 73.92, '1 Attack Damage' : -15.83, '1 Health' : -1.44,
                            '1 Power' : -320.01, '1 Spawn Time' : 104.78, '.001 Critical Chance' : -29.83,
                            '.1 Critical Multiplier' : -16.26}
    #negative coefficient is multiplied by (player_stat - average_stat) if player_stat < average_stat

    size = len(players)

    avg_power = float(mean([player.power for player in players]))
    avg_atk_dmg = float(mean([player.atk_dmg for player in players]))
    avg_atk_spd = float(mean([player.atk_spd for player in players]))
    avg_crit_x = float(mean([player.crit_x for player in players]))
    avg_crit_pct = float(mean([player.crit_pct for player in players]))
    avg_health = float(mean([player.max_health for player in players]))
    avg_spawn = float(mean([player.spawn_time for player in players]))

    avg_power = round(avg_power)
    avg_atk_dmg = round(avg_atk_dmg)
    avg_atk_spd = round(avg_atk_spd)
    avg_crit_x = round(avg_crit_x, 2)
    avg_crit_pct = round(avg_crit_pct, 4)
    avg_health = round(avg_health, 2)
    avg_spawn = round(avg_spawn)

    for player in players:

        if player.power > avg_power:
            player.grade_dict['Power'] = (player.power - avg_power) * pos_xWAR_coefficient['1 Power']
        elif player.power < avg_power:
            player.grade_dict['Power'] = -(player.power - avg_power) * neg_xWAR_coefficient['1 Power']
        elif player.power == avg_power:
            player.grade_dict['Power'] = 0

        if player.atk_dmg > avg_atk_dmg:
            player.grade_dict['Attack Damage'] = (player.atk_dmg - avg_atk_dmg) * pos_xWAR_coefficient['1 Attack Damage']
        elif player.atk_dmg < avg_atk_dmg:
            player.grade_dict['Attack Damage'] = -(player.atk_dmg - avg_atk_dmg) * neg_xWAR_coefficient['1 Attack Damage']
        elif player.atk_dmg == avg_atk_dmg:
            player.grade_dict['Attack Damage'] = 0

        if player.atk_spd > avg_atk_spd:
            player.grade_dict['Attack Speed'] = (player.atk_spd - avg_atk_spd) * pos_xWAR_coefficient['1 Attack Speed']
        elif player.atk_spd < avg_atk_spd:
            player.grade_dict['Attack Speed'] = -(player.atk_spd - avg_atk_spd) * neg_xWAR_coefficient['1 Attack Speed']
        elif player.atk_spd == avg_atk_spd:
            player.grade_dict['Attack Speed'] = 0

        if player.crit_x > avg_crit_x:
            player.grade_dict['Critical-X'] = (10*(player.crit_x - avg_crit_x)) * pos_xWAR_coefficient['.1 Critical Multiplier']
        elif player.crit_x < avg_crit_x:
            player.grade_dict['Critical-X'] = -(10*(player.crit_x - avg_crit_x)) * neg_xWAR_coefficient['.1 Critical Multiplier']
        elif player.crit_x == avg_crit_x:
            player.grade_dict['Critical-X'] = 0

        if player.crit_pct > avg_crit_pct:
            player.grade_dict['Critical-PCT'] = (1000*(player.crit_pct - avg_crit_pct)) * pos_xWAR_coefficient['.001 Critical Chance']
        elif player.crit_pct < avg_crit_pct:
            player.grade_dict['Critical-PCT'] = -(1000 * (player.crit_pct - avg_crit_pct)) * neg_xWAR_coefficient['.001 Critical Chance']
        elif player.crit_pct == avg_crit_pct:
            player.grade_dict['Critical-PCT'] = 0

        if player.max_health > avg_health:
            player.grade_dict['Health'] = (player.health - avg_health) * pos_xWAR_coefficient['1 Health']
        elif player.max_health < avg_health:
            player.grade_dict['Health'] = -(player.health - avg_health) * neg_xWAR_coefficient['1 Health']
        elif player.max_health == avg_health:
            player.grade_dict['Health'] = 0

        if player.spawn_time > avg_spawn:
            player.grade_dict['Spawn'] = (player.spawn_time - avg_spawn) * pos_xWAR_coefficient['1 Spawn Time']
        elif player.spawn_time < avg_spawn:
            player.grade_dict['Spawn'] = -(player.spawn_time - avg_spawn) * neg_xWAR_coefficient['1 Spawn Time']
        elif player.spawn_time == avg_spawn:
            player.grade_dict['Spawn'] = 0

        for word in ['Power', 'Attack Damage', 'Attack Speed', 'Critical-X', 'Critical-PCT', 'Health', 'Spawn']:
            player.grade_dict[word] = round(player.grade_dict[word], 2)

        player.xWAR = round((player.grade_dict['Power'] + player.grade_dict['Attack Damage'] + player.grade_dict['Attack Speed']
        + player.grade_dict['Critical-X'] + player.grade_dict['Critical-PCT'] + player.grade_dict['Health'] + player.grade_dict['Spawn']), 2)

    players.sort(key=lambda pl: pl.xWAR, reverse=True)
    rank_index = 0
    for player in players:
        player.grade_dict['Rank'] = 1 + rank_index
        rank_index += 1

def write_to_file(filename=None, words=None, mode='w', error=False):
    if error:
        filename = 'error_output'
        mode = 'a'

    with open(filename, mode) as f:
        f.write(words + '\n')

def generate_lineups_six_to_four(six_lineup):
    #this will take in a single lineup of SIX players and return 9 lineups
    #there are the 8 best lineups, and the 9th is the best lineup again
    four_lineups = [0,1,2,3,4,5,6,7,8]
    six_lineup.sort(key=lambda player : player.xWAR, reverse=True)
    four_lineups[0] = [six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[3]]
    four_lineups[1] = [six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[4]]
    four_lineups[2] = [six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[5]]
    four_lineups[3] = [six_lineup[0], six_lineup[1], six_lineup[3], six_lineup[4]]
    four_lineups[4] = [six_lineup[0], six_lineup[1], six_lineup[3], six_lineup[5]]
    four_lineups[5] = [six_lineup[0], six_lineup[1], six_lineup[4], six_lineup[5]]
    four_lineups[6] = [six_lineup[0], six_lineup[2], six_lineup[3], six_lineup[4]]
    four_lineups[7] = [six_lineup[0], six_lineup[2], six_lineup[3], six_lineup[5]]
    four_lineups[8] = [six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[3]]

    #0: all lineups (9), 1: all but 6 and 7 (7),
    #2: [0,1,2,6,7,8] (6), 3: [0,3,4,6,7] (6)
    #4: [1,3,5,6,8] (4) 5: [2,4,5,7] (4)
    return four_lineups

class Team:

    names = ["Phoenixes", "Dragons", "Banshees", "Wraiths", "Specters", "Revenants", "Seraphs", "Chimera", "Gorgons",
             "Minotaurs", "Harpies", "Mermaids", "Naga", "Satyrs", "Centaur", "Unicorns", "Griffins", "Rocs",
             "Sphinxes", "Cyclops", "Titans", "Fates", "Valkyries", "Demigods", "Godkillers", "Inferno", "Hive", "Elementals", "Golems",
             "Ifrits", "Djinni", "Imps", "Sprites", "Goblins", "Trolls", "Orcs", "Zombies", "Ghosts", "Werewolves",
             "Vampires", "Liches", "Slayers", "Faeries", "Elves", "Dwarves", "Gnomes",
             "Halflings", "Ogres", "Giants", "Hydras", "Krakens", "Leviathan", "Serpents", "Basilisks",
             "Manticores", "Wyrms", "Wyverns", "Behemoths", "Manticore", "Harpy", "Merfolk", "Naiads",
             "Dryads", "Sirens", "Eladrin", "Draconians", "Demons", "Angelkin", "Succubi", "Incubi",
             "Oni", "Kitsune", "Rakshasa", "Feykin", "Impalers", "Necromancers", "Warlocks",
             "Enchanters", "Shamans", "Sorcerers", "Illusionists", "Geomancers", "Chronomancers",
              "Diviners",  "Magi", "Alchemists", "Witchdoctors", "Arcanists", "Summoners",
             "Purifiers", "Exorcists", "Warden", "Guardians", "Protectors", "Crusaders", "Paladins", "Armament", "Gravity", "Assassins",
             "Templars", "Inquisitors", "Acolytes", "Clerics", "Priests", "Druids", "Shapeshifters", "Skinwalkers",
             "Warg", "Beastmasters",  "Dervish", "Puppeteer", "Psychic", "Oracle", "Mystic", "Tar-Creepers", "Amalgam", 'Wings', 'Termites', 'Revolution',
             'Arch-Kings', 'Samurai', 'Darkness', 'Voidwalkers', 'Ghasts', 'Watchers', 'Bloodspawn', 'Night-Terrors', 'Underlords', 'Devils',
             'Serpents', 'Swashbucklers', 'Sunspots']

    names = list(set(names))
    names_copy = names.copy()

    def __init__(self,region,mine=False,pre_name=None):
        seed()
        if pre_name:
            b = pre_name
        elif Team.names:
            b = choice(Team.names)
            Team.names.remove(b)
        else:
            Team.names = [f"+{name}" for name in Team.names]

            b = choice(Team.names_copy)
        n = f"{region}_{b}"
        self.mine = mine
        if self.mine:
            self.name = f"**{n}**"
        else:
            self.name = n
        self.region = region
        self.full_name = self.name

        #ALL DONE: here, make it so that each team is given six players, and 15 lineups of 4 arranged from these players
        # will be saved in self.lineups which is a list of player lists
        # each team will also get a lineup_wins list and a lineup_losses list
        # and the number of wins/losses that lineup has
        # this will initiate the full lineup of six (team.players object) and generate...() will be run AFTER
        #todo play with team creation wth 6-man rosters to ensure a decent amount of variability
        if region == 'House-of-Achlys':
            self.players = [s_tier(), c_tier(2.5), c_tier(2), c_tier(1.75), a_tier(1), b_tier(1.2)]
        elif region == 'Universal':
            self.players = [s_tier(), a_tier(), b_tier(round(uniform(1,2),2)), c_tier(0.5), c_tier(1), b_tier(round(uniform(1,2),2))]
        elif region == 'Labyrinth':
            self.players = [s_tier(), a_tier(round(uniform(1,2),2)), b_tier(round(uniform(1,2),2)), b_tier(1), b_tier(0.5), c_tier()]
        elif region == 'Test':
            self.players = [s_tier(round(uniform(1,3),2)), a_tier(round(uniform(1,4),2)),
                            b_tier(round(uniform(0.5,5),2)), b_tier(round(uniform(0.5,5),2)),
                            c_tier(round(uniform(0,6),2)), c_tier(round(uniform(0,7),2))]
        else:
            self.players = [s_tier(), a_tier(1), a_tier(), b_tier(1), c_tier(), c_tier(round(uniform(1,2),2))]
        grade_players(self.players)
        self.players.sort(key= lambda p : p.grade_dict["Rank"])
        all_lineups = list(generate_lineups_six_to_four(self.players))
        self.lineups = all_lineups

        # this lineups object is a LIST OF LISTS

        for player in self.players:
            player.team = self.name
        self.wins = 0
        self.losses = 0
        #the two below values hold wins and losses for total, 15-lineup regular season series. they are not used for
        # computing standings
        self.match_wins = 0
        self.match_losses = 0
        self.match_draws = 0

        self.lineup_wins = [0] * 15
        self.lineup_losses = [0] * 15

        self.points  = -1

        self.trophies = 0
        self.seed = -1
        self.history = {0 : "", 1 : "", 2 : "", 3 : "", 4 : "", 5 : "", 6 : "", 7 : "", 8 : "", 9 : "", 10 : ""}
        #self.seed_dict = {'RegionRegular' : -1, 'RegionPlayoffs' : -1, 'UniPlayIn' : -1, 'UniGroup' : -1, 'UniRegular' : -1}
        self.group = "None"
        self.margin = 0
        self.accolades = {'Regional-Playoffs' : 0, 'Regional-Champ' : 0, 'Last-Stand' : 0, 'Pre-Qualifying' : 0, 'Universal-Qualifying' : 0, 'Universal-Playoffs' : 0, 'Uni-Playoff-Wins' : 0, 'Universal-Champ' : 0}
        #self.generate_player_names()

        #0 means no second round pick, 1 means group 1 (missed regional playoffs) and 2 means group 2 (came from region
        # and made PQ or further)
        self.second_pick = 0
        self.third_pick = 0

        self.qualifying_group = 0

    def make_mine(self):
        self.mine = True
        self.name = f"**{self.name}**"

    def print_team_name(self, season_count):
        if self.mine:
            with open('my_teams', 'a') as m:
                m.write(f"S{season_count}_{self.name}\n")
        with open('history', 'a') as h:
            h.write(f"S{season_count}_{self.name}\n")

    def print_team_info(self,test=False):

        if not test:
            print(Fore.RED + Back.CYAN + Style.BRIGHT + f"{self.full_name.upper()}" + Style.RESET_ALL)
            print(Fore.RED + Back.CYAN + Style.BRIGHT + f"Wins: {self.wins} ({round((self.wins/(self.wins+self.losses)*100),2)}%)"
                  + Style.RESET_ALL)
            print(Fore.RED + Back.CYAN + Style.BRIGHT + f"Losses: {self.losses}" + Style.RESET_ALL)
        for player in self.players:
            print(str(player))

    def print_history(self, season_count):
        if self.mine:
            with open('my_teams', 'a') as h:
                if season_count != 1:
                    for s in range(1, season_count + 1):
                        h.write(f"Season {s}: {self.history[s]}\n")
                else:
                    h.write(f"Season 1: {self.history[1]}\n")
                h.write('--------------\n')
        with open('history', 'a') as h:
            if season_count != 1:
                for s in range(1, season_count + 1):
                    h.write(f"Season {s}: {self.history[s]}\n")
            else:
                h.write(f"Season 1: {self.history[1]}\n")
            h.write('--------------\n')

    def print_accolades(self):
        if self.mine:
            with open('my_teams', 'a') as h:
                i = 0
                for key in self.accolades.keys():
                    h.write(f"{key}: {self.accolades[key]}, ")
                    i += 1
                    if i % 4 == 0:
                        h.write('\n')
                h.write('\n')

        with open('history', 'a') as h:
            i=0
            for key in self.accolades.keys():
                h.write(f"{key}: {self.accolades[key]}, ")
                i+=1
                if i%4 == 0:
                    h.write('\n')
            h.write('\n')

    def most_kills_on_team(self):
        max_kills = 0
        index = 0
        for player in self.players:
            if player.kills > max_kills:
                max_kills = player.kills
                max_index = index
            index += 1
        return self.players[max_index]

    def sort_players_by_tier(self):
        players = self.players
        tier_order = {'S': 4, 'A': 3, 'B': 2, 'C': 1}  # Map tier characters to numerical values
        sorted_players = sorted(players, key=lambda p: (tier_order[p.tier], p.power), reverse=True)
        return sorted_players

    def print_roster(self,finale=False):
        if self.mine:
            print(f"{self.name.upper()} ROSTER\n")
            i = 0
            for player in self.players:
                print(f"({i})")
                i += 1
                print(str(player))
            print('\n----------------------\n')
        else:
            if not finale:
                with open('rosters', 'a', buffering=1) as f:
                    f.write(f"{self.name.upper()} ROSTER\n\n")
                    i = 0
                    for player in self.players:
                        f.write(f"({i})\n")
                        i += 1
                        f.write(str(player))
                    f.write('\n----------------------\n\n')
            else:
                with open('rosters', 'w', buffering=1) as f:
                    f.write(f"{self.name.upper()} ROSTER\n\n")
                    i = 0
                    for player in self.players:
                        f.write(f"({i})\n")
                        i += 1
                        f.write(str(player))
                    f.write('\n----------------------\n\n')


    def trade(self, other):
        rec_index = input("Enter the index of the player being received.")
        trad_index = input("Enter the index of the player being traded.")

