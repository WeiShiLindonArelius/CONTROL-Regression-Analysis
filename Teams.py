from random import choice, seed, uniform
from Player_Creator import s_tier, a_tier, b_tier, c_tier, slasher, undead
from colorama import Fore, Back, Style
from numpy import mean
from stat_functions import QUERY

import itertools

def grade_players(players, is_team=None):
    #should take in a list of players, not a dict draft class

    pos_xWAR_coefficient = {'1 Attack Speed' : -61.46, '1 Attack Damage' : 16.67, '1 Health' : 0.34,
                            '1 Power' : 250, '1 Spawn Time' : -149.98, '.001 Critical Chance' : 26.40,
                            '.1 Critical Multiplier' : 0.79}
    #positive coefficient is multiplied by (player_stat - average_stat) if player_stat > average_stat
    #pos coefficient = stat goes UP by X, xWAR goes UP by Y (so negative numbers mean xWAR goes DOWN)

    neg_xWAR_coefficient = {'1 Attack Speed' : 73.92, '1 Attack Damage' : -15.83, '1 Health' : -1.44,
                            '1 Power' : -250, '1 Spawn Time' : 104.78, '.001 Critical Chance' : -29.83,
                            '.1 Critical Multiplier' : -16.26}
    #negative coefficient is multiplied by (player_stat - average_stat) if player_stat < average_stat
    #neg coefficient = stat goes DOWN by X, xWAR goes UP by Y (so negative numbers mean xWAR goes DOWN)
    #coefficients for power have been adjusted to +/- 250

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
    four_lineups = []
    six_lineup.sort(key=lambda player : player.xWAR, reverse=True)
    four_lineups.append([six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[3]])
    four_lineups.append([six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[4]])
    four_lineups.append([six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[5]])
    four_lineups.append([six_lineup[0], six_lineup[1], six_lineup[3], six_lineup[4]])
    four_lineups.append([six_lineup[0], six_lineup[1], six_lineup[3], six_lineup[5]])
    four_lineups.append([six_lineup[0], six_lineup[1], six_lineup[4], six_lineup[5]])
    four_lineups.append([six_lineup[0], six_lineup[2], six_lineup[3], six_lineup[4]])
    four_lineups.append([six_lineup[0], six_lineup[2], six_lineup[3], six_lineup[5]])
    four_lineups.append([six_lineup[0], six_lineup[1], six_lineup[2], six_lineup[3]])

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
             "Halflings", "Ogres", "Hydra", "Kraken", "Leviathan", "Serpents", "Basilisks", "Wendigo",
            "Wyverns", "Behemoths", "Manticore", "Naiads", "Frostlords", "Ghost-Runners", "Ents", "Terraformers",
             "Dryads", "Sirens", "Eladrin", "Draconians", "Demons", "Angelkin", "Succubi", "Incubi", "Nebulae",
             "Oni", "Kitsune", "Rakshasa", "Feykin", "Impalers", "Necromancers", "Warlocks", "Lunatics",
             "Enchanters", "Shamans", "Sorcerers", "Illusionists", "Geomancers", "Chronomancers", "Aether",
              "Diviners",  "Magi", "Alchemists", "Witchdoctors", "Arcanists", "Summoners", "Zealots", "Thunderbirds",
             "Purifiers", "Exorcists", "Warden", "Guardians", "Protectors", "Crusaders", "Paladins", "Armament", "Gravity", "Assassins",
             "Templars", "Inquisitors", "Acolytes", "Clerics", "Priests", "Druids", "Shapeshifters", "Skinwalkers",
             "Warg", "Beastmasters",  "Dervish", "Puppeteer", "Psychic", "Oracle", "Mystic", "Tar-Creepers", "Amalgam", 'Wings', 'Termites', 'Revolution',
             'Arch-Kings', 'Samurai', 'Darkness', 'Voidwalkers', 'Ghasts', 'Watchers', 'Bloodspawn', 'Night-Terrors', 'Underlords', 'Devils',
             'Swashbucklers', 'Sunspots', "Aces", "Fever", "Mavericks", "Rangers"]

    names = list(set(names))
    names_copy = names.copy()

    def __init__(self,region,mine=False,pre_name=None,season_count=-1):
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
        if self.mine and '*' not in n:
            self.name = f"**{n}**"
        else:
            self.name = n
        self.region = region
        self.season_origin = season_count
        self.full_name = self.name

        team_sql = """ 
                INSERT INTO Team(team_name, region_of_origin, season_of_origin)
                VALUES (?, ?, ?)
        """
        team_params = (self.name, self.region, self.season_origin)
        self.team_id = QUERY(team_sql, params=team_params, is_select=False)
        #QUERY is set to return the primary key assigned to a created value

        #ALL DONE: here, make it so that each team is given six players, and 15 lineups of 4 arranged from these players
        # will be saved in self.lineups which is a list of player lists
        # each team will also get a lineup_wins list and a lineup_losses list
        # and the number of wins/losses that lineup has
        # this will initiate the full lineup of six (team.players object) and generate...() will be run AFTER

        if region == 'Universal':
            uni_coin = choice([1,2,3,4])

            if uni_coin == 1:
                coin_player = s_tier(round(uniform(0,2),2), season_count=season_count, trait_amp=.99)
            elif uni_coin == 2:
                coin_player = a_tier(round(uniform(0,2.5), 2), season_count=season_count, trait_amp=0.98)
            elif uni_coin == 3:
                coin_player = b_tier(round(uniform(0, 3), 2), season_count=season_count, trait_amp=0.95)
            else:
                coin_player = c_tier(round(uniform(0, 4.5), 2), season_count=season_count, trait_amp=0.9)


            self.players = [s_tier(round(uniform(0,4),2), season_count=season_count), a_tier(round(uniform(1,4),2), season_count=season_count), b_tier(round(uniform(1,4),2), season_count=season_count), c_tier(round(uniform(2,5),2), season_count=season_count), c_tier(round(uniform(0,6),2), season_count=season_count), coin_player]

        elif region == 'Labyrinth':
            self.players = [s_tier(season_count=season_count, trait_amp=0.8),
                            a_tier(round(uniform(1,2),2), season_count=season_count, trait_amp=0.75),
                            b_tier(round(uniform(1,2),2), season_count=season_count, trait_amp=0.7),
                            b_tier(1, season_count=season_count, trait_amp=0.65),
                            b_tier(0.5, season_count=season_count, trait_amp=0.6),
                            c_tier(season_count=season_count, trait_amp=0.5, pre_reflect=1)]
        elif region == 'Test':
            self.players = [s_tier(round(uniform(1,3),2), season_count=season_count), a_tier(round(uniform(1,4),2), season_count=season_count),
                            b_tier(round(uniform(0.5,5),2), season_count=season_count), b_tier(round(uniform(0.5,5),2), season_count=season_count),
                            c_tier(round(uniform(0,6),2), season_count=season_count), c_tier(round(uniform(0,7),2), season_count=season_count)]
        elif region == 'Cosmic':
            self.players = [slasher(round(uniform(0,2.5),2), season_count=season_count), slasher(round(uniform(0,2.25),2), season_count=season_count),
                            slasher(round(uniform(0,2),2), season_count=season_count), slasher(round(uniform(0,1.75),2), season_count=season_count),
                            slasher(round(uniform(0,1.5),2), season_count=season_count), slasher(round(uniform(0,1.25),2), season_count=season_count)]
        elif region == 'Tartarus':
            self.players = [undead(round(uniform(0, 3), 2), season_count=season_count),
                            undead(round(uniform(0, 3), 2), season_count=season_count),
                            undead(round(uniform(0, 2.5), 2), season_count=season_count),
                            undead(round(uniform(0, 2.5), 2), season_count=season_count),
                            undead(round(uniform(0, 1.25), 2), season_count=season_count),
                            undead(round(uniform(0, 1.25), 2), season_count=season_count)]
        elif region == 'Beyond':
            self.players = [s_tier(round(uniform(0, 4), 2), season_count=season_count, pre_reflect=1),
                            a_tier(round(uniform(1, 4), 2), season_count=season_count, pre_reflect=1),
                            b_tier(round(uniform(0.5, 4.5), 2), season_count=season_count, pre_reflect=1),
                            b_tier(round(uniform(1.5, 3.5), 2), season_count=season_count, pre_reflect=1),
                            c_tier(round(uniform(3, 4), 2), season_count=season_count, pre_reflect=1),
                            c_tier(round(uniform(2, 6.5), 2), season_count=season_count, pre_reflect=1)]


        else:
            self.players = [s_tier(round(uniform(0,1)), season_count=season_count),
                            a_tier(round(uniform(0,(1.5 if choice([True, False]) else 0.5)),2), season_count=season_count, trait_amp=0.95),
                            b_tier(round(uniform(1,(2.5 if choice([True, False, False]) else 4)),2), season_count=season_count),
                            (b_tier(round(uniform(0, 2.5)), season_count=season_count) if choice([True, True, False]) else a_tier(round(uniform(0, 2.5)),season_count=season_count,fixed=choice(['C%','I*','Pp']))),
                            (c_tier(round(uniform(0, 2.5)), season_count=season_count) if choice([True, True, False]) else slasher(round(uniform(0, 2.5)),season_count=season_count)),
                            (c_tier(round(uniform(0, 2.5)), season_count=season_count) if choice([True, True, False]) else undead(round(uniform(0, 1)),season_count=season_count))]


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
        self.region_seed = "None"
        self.history = {key: "" for key in range(50)}
        #self.seed_dict = {'RegionRegular' : -1, 'RegionPlayoffs' : -1, 'UniPlayIn' : -1, 'UniGroup' : -1, 'UniRegular' : -1}
        self.group = "None"
        self.played_region = {key: "" for key in range(50)} # dictionary of the leagues a team played in. keys
                                                            # are season_count, vals a string assigned in  league_season

        self.margin = 0
        self.accolades = {'Regional-Playoffs' : 0, 'Regional-Champ' : 0, 'Last-Stand' : 0, 'Pre-Qualifying' : 0,
                          'Universal-Qualifying' : 0, 'Universal-League' : 0, 'Universal-Playoffs' : 0, 'Uni-Playoff-Wins' : 0, 'Universal-Champ' : 0
                          , 'Slashers' : 0, 'Undead' : 0, 'Reflectors' : 0
                          , 'Clutch Players' : 0, 'Inconsistent Players' : 0, 'Playoff Performers' : 0}
        #self.generate_player_names()

        #0 means no second round pick, 1 means group 1 (missed regional playoffs) and 2 means group 2 (came from region
        # and made PQ or further)
        self.second_pick = 0
        self.third_pick = 0

        self.qualifying_group = 0

    def make_mine(self,name):
        self.mine = True
        self.name = f"**{name}**" if "**" not in name else name

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
                h.write('--------------\n\n')
        with open('history', 'a') as h:
            if season_count != 1:
                for s in range(1, season_count + 1):
                    h.write(f"Season {s}: {self.history[s]}\n")
            else:
                h.write(f"Season 1: {self.history[1]}\n")
            h.write('--------------\n\n')

    def print_accolades(self):
        undead_count = 0
        slasher_count = 0
        reflector_count = 0
        clutch_count = 0
        inc_count = 0
        pp_count = 0
        for player in self.players:
            if player.trait_tag == 'U-':
                undead_count += 1
            elif player.trait_tag == '$l':
                slasher_count += 1
            elif player.trait_tag == 'R#':
                reflector_count += 1
            elif player.trait_tag == 'C%':
                clutch_count += 1
            elif player.trait_tag == 'I*':
                inc_count += 1
            elif player.trait_tag == 'Pp':
                pp_count += 1
        self.accolades['Slashers'] = slasher_count
        self.accolades['Undead'] = undead_count
        self.accolades['Reflectors'] = reflector_count
        self.accolades['Clutch Players'] = clutch_count
        self.accolades['Inconsistent Players'] = inc_count
        self.accolades['Playoff Performers'] = pp_count

        if self.mine:
            with open('my_teams', 'a') as h:
                i = 0
                for key in self.accolades.keys():
                    h.write(f"{key}: {self.accolades[key]}")
                    if i <= len(self.accolades.keys())-1:
                        h.write(", ")
                    i += 1
                    if i % 4 == 0:
                        h.write('\n')
                h.write('\n')

        with open('history', 'a') as h:
            i=0
            for key in self.accolades.keys():
                h.write(f"{key}: {self.accolades[key]}")
                if i <= len(self.accolades.keys()) - 1:
                    h.write(", ")
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

