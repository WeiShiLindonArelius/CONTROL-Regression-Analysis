from random import uniform, seed, choice

import pandas as pd
from colorama import Fore, Style
import math
import numpy as np
from collections import OrderedDict

def write_to_file(filename=None, words=None, mode='w', error=False):
    if error:
        filename = 'error_output'
        mode = 'a'

    with open(filename, mode) as f:
        f.write(words + '\n')

def ordinal_string(n: int) -> str:
    if 10 <= n % 100 < 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    if n == 0:
        suffix = ''
    return f"{n}{suffix}"

def calculate_standard_deviation(number, sample_size, sample_average):
    deviation = number - sample_average
    standard_deviation = deviation / math.sqrt(sample_size)
    return standard_deviation


def grade_seasons(seasons, print_averages=False, import_averages = None, context = None, avg_stats_df = None, region=None):

    DATA_FRAME = False

    #todo at the moment, this is creating a new DF for each player season and appending it to the  excel file in both
    # best_of_stats and region_mvp, massively slowing down the code
    # adding a check for region  == 'All' makes it so that only one player gets added to the sheet for some reason

    MULT_NO_USE = True
    full_season = False
    avg_stats_df = None

    #iterate through each object, and create lists with values corresponding to each player
    #put each list through calculate_standard_deviations and use it to assign a coefficient variable to each player equivalent
    #a total season's grade is determined by the sum of all coefficients

    #the import_averages function is for when seasons are being graded for a team, so their season grades can be compared to those of the league they were in
    #instead of just the team

    STANDARD_LENGTH = 50

    trash = choice(seasons)
    game_length = trash.game_length
    multiplier = 1 if MULT_NO_USE else STANDARD_LENGTH / game_length

    if import_averages:
        size = len(import_averages)

        total_kills = 0
        total_deaths = 0
        total_damage = 0
        total_effect = 0
        total_overkill = 0
        total_mitigated = 0

        kills_list = []
        deaths_list = []
        damage_list = []
        effect_list = []
        overkill_list = []
        mitigated_list = []

        if DATA_FRAME:
            for season in import_averages:
                path = 'C:/Users/carte/OneDrive/Documents/PlayerSeasons.xlsx'

                existing_df = pd.read_excel(path)

                szn_df = pd.DataFrame(
                    columns=['Name', 'Team', 'Kills', 'Deaths', 'Damage', 'Effect', 'Overkill', 'Mitigated'])
                szn_dict = {'Name': season.player.name, 'Team': season.player.team, 'Kills': season.kills,
                            'Deaths': season.deaths, 'Damage': season.damage, 'Effect': season.effect,
                            'Overkill': season.overkill, 'Mitigated': season.mitigated}
                szn_dict_df = pd.DataFrame([szn_dict])
                szn_df = pd.concat([szn_df, szn_dict_df])
                final_df = pd.concat([existing_df, szn_df], ignore_index=True)

                with pd.ExcelWriter(path, engine='openpyxl') as writer:
                    final_df.to_excel(writer, sheet_name='PlayerSeasonStats', index=False)

        for season in import_averages:

            kills_list.append(season.kills*multiplier)
            deaths_list.append(season.deaths*multiplier)
            damage_list.append(season.damage*multiplier)
            effect_list.append(season.effect*multiplier)
            overkill_list.append(season.overkill*multiplier)
            mitigated_list.append(season.mitigated*multiplier)

            total_kills += season.kills * multiplier
            total_deaths += season.deaths * multiplier
            total_damage += season.damage * multiplier
            total_effect += season.effect * multiplier
            total_overkill += season.overkill * multiplier
            total_mitigated += season.mitigated * multiplier
    else:
        size = len(seasons)

        total_kills = 0
        total_deaths = 0
        total_damage = 0
        total_effect = 0
        total_overkill = 0
        total_mitigated = 0

        kills_list = []
        deaths_list = []
        damage_list = []
        effect_list = []
        overkill_list = []
        mitigated_list = []

        if DATA_FRAME:
            for season in seasons:
                path = 'C:/Users/carte/OneDrive/Documents/PlayerSeasons.xlsx'

                existing_df = pd.read_excel(path)

                szn_df = pd.DataFrame(
                    columns=['Name', 'Team', 'Kills', 'Deaths', 'Damage', 'Effect', 'Overkill', 'Mitigated'])
                szn_dict = {'Name': season.player.name, 'Team': season.player.team, 'Kills': season.kills,
                            'Deaths': season.deaths, 'Damage': season.damage, 'Effect': season.effect,
                            'Overkill': season.overkill, 'Mitigated': season.mitigated}
                szn_dict_df = pd.DataFrame([szn_dict])
                szn_df = pd.concat([szn_df, szn_dict_df])
                final_df = pd.concat([existing_df, szn_df], ignore_index=True)

                with pd.ExcelWriter(path, engine='openpyxl') as writer:
                    final_df.to_excel(writer, sheet_name='PlayerSeasonStats', index=False)

        for season in seasons:

            kills_list.append(season.kills * multiplier)
            deaths_list.append(season.deaths * multiplier)
            damage_list.append(season.damage * multiplier)
            effect_list.append(season.effect * multiplier)
            overkill_list.append(season.overkill * multiplier)
            mitigated_list.append(season.mitigated * multiplier)

            total_kills += season.kills * multiplier
            total_deaths += season.deaths * multiplier
            total_damage += season.damage * multiplier
            total_effect += season.effect * multiplier
            total_overkill += season.overkill * multiplier
            total_mitigated += season.mitigated * multiplier

    try:
        avg_kills = total_kills / size
        avg_deaths = total_deaths / size
        avg_damage = total_damage / size
        avg_effect = total_effect / size
        avg_overkill = total_overkill / size
        avg_mitigated = total_mitigated / size

#        with open('error_output', 'a') as e:
#            e.write(f"\n{context}League KD stats: {total_kills:.3f} total kills, {total_deaths:.3f} total deaths\n"
#                    f"{avg_kills:.3f} average kills, {avg_deaths:.3f} average deaths.")
#            if total_deaths == total_kills and avg_deaths == avg_kills:
#                e.write("(Values Equal)\n")
#            else:
#                e.write("(Values Unequal)\n")


    except ZeroDivisionError:
        avg_kills = -1
        avg_deaths = -1
        avg_damage = -1
        avg_effect = -1
        avg_overkill = -1
        avg_mitigated = -1

    average_stats_num = {'Kills': avg_kills, 'Deaths': avg_deaths, 'Damage': avg_damage, 'Effect': avg_effect, 'Overkill': avg_overkill, 'Mitigated': avg_mitigated}
    stat_words = ['Kills', 'Deaths', 'Damage', 'Effect', 'Overkill', 'Mitigated']

    if not region:
        region = 'Error'

    if DATA_FRAME:
        stats_df_values = {'Region' : region, 'Kills': avg_kills, 'Deaths': avg_deaths, 'Damage': avg_damage, 'Effect': avg_effect, 'Overkill': avg_overkill, 'Mitigated': avg_mitigated}
        stats_to_append = pd.DataFrame([stats_df_values])

        stats_df_cols = ['Region', 'Kills', 'Deaths', 'Damage', 'Effect', 'Overkill', 'Mitigated']
        avg_stats_df = pd.DataFrame(columns=stats_df_cols)
        avg_stats_df = pd.concat([avg_stats_df, stats_to_append], ignore_index=True)
        #avg_stats_df is a one row dataframe with the values for this season only.
        #it is to be appended to existing_df, which reads from the Excel file.

        path = "C:/Users/carte/OneDrive/Documents/ControlAverageStats.xlsx"
        existing_df = pd.read_excel(path) # replace with  = pd.DataFrame(columns=stats_df_cols) to clear data
        final_df = pd.concat([existing_df, avg_stats_df], ignore_index=True)

        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            final_df.to_excel(writer, sheet_name='AverageSeasonStats', index=False)


    average_stats_list = {'Kills' : kills_list, 'Deaths' : deaths_list, 'Damage' : damage_list, 'Effect' : effect_list,
                          'Overkill' : overkill_list, 'Mitigated' : mitigated_list}

    for season in seasons:

        if print_averages:
            season.grade_breakdown += f"Avg Kills: {avg_kills:.3f}, Avg Deaths: {avg_deaths:.3f}, Avg Damage: {avg_damage:.3f},\n Avg Effect: {avg_effect:.3f}," \
                                      f"Avg Overkill: {avg_overkill:.3f}, Avg Mitigated: {avg_mitigated:.3f}\n"

        weights = {'Kills': 4, 'Deaths': -3, 'Damage': 0.75, 'Effect': 7, 'Overkill': 0.25, 'Mitigated': 0.2}


        translate = {'Kills' : season.kills*multiplier, 'Deaths' : season.deaths*multiplier, 'Damage' : season.damage*multiplier, 'Effect' : season.effect*multiplier,
                     'Overkill' : season.overkill*multiplier, 'Mitigated' : season.mitigated*multiplier}

        iqr_stats = {}

        for word in stat_words:
            #iqr_stats contains is a dictionary which contains the word for each stat as a key, and the difference between the
            # 1st and 3rd quartiles as a value for each stat
            iqr_stats[word] = np.percentile(average_stats_list[word], 75) - np.percentile(average_stats_list[word], 25)
            season.league_averages[word] = round(average_stats_num[word], 3)

        #the next thing to do is find the difference between the average stat and player stat for each season,
        #and DIVIDE this number by the interquartile range to get the normalized difference between the average and player stat
        #then, multiply each normalized difference by the chosen weights, and add everything together to get the total grade

        norm_differences = {}

        for word in stat_words:
            if iqr_stats[word] != 0:
                norm_differences[word] = (translate[word] - average_stats_num[word]) / iqr_stats[word]
            elif word != 'Overkill':
                norm_differences[word] = (translate[word] - average_stats_num[word])
            else:
                norm_differences[word] = (translate[word] - average_stats_num[word]) / 10000
            season.season_grade_dict[word] = norm_differences[word] * weights[word]

        season.season_grade_data = (season.season_grade_dict['Kills']) + (season.season_grade_dict['Deaths']) + (season.season_grade_dict['Damage']) + (season.season_grade_dict['Effect']) + (season.season_grade_dict['Overkill']) + (season.season_grade_dict['Mitigated'])
        season.grade_breakdown += f"{season.season_grade_dict['Kills']:.3f} in kills * 5, {season.season_grade_dict['Deaths']:.3f} in deaths * -5, {season.season_grade_dict['Damage']:.3f} in damage / 2,\n{season.season_grade_dict['Effect']:.3f} in effect * 10, {season.season_grade_dict['Overkill']:.3f} in overkill effect / 4, {season.season_grade_dict['Mitigated']:.3f} in mitigated / 5."


    # takes in a list of PlayerSeason objects

class PlayerSeason:
    def __init__(self, player, season_count, sub_season=None):
        #sub_season is for a PlayerSeason object is being created only for one part of the season, such as the regional regular season
        #this will be a string value

        self.season = season_count
        self.player = player
        self.age = self.player.age
        self.game_count = player.games_played['This-Season']
        self.match_count = player.games_played['Matches']
        self.sub_season = sub_season
        self.season_grade_dict = {'Kills' : 0, 'Deaths' : 0, 'Damage' : 0, 'Effect' : 0, 'Overkill' : 0, 'Mitigated' : 0}
        self.league_averages = {'Kills' : 0, 'Deaths' : 0, 'Damage' : 0, 'Effect' : 0, 'Overkill' : 0, 'Mitigated' : 0}
        self.season_grade_data = 0
        self.grade_breakdown = ""
        self.game_length = player.game_length
        if self.game_count != 0:
            self.kills = player.kills / self.game_count
            self.deaths = player.deaths / self.game_count
            self.damage = player.damage_data['Total-Damage'] / self.game_count
            self.effect = player.damage_data['Tesseract'] / self.game_count
            self.overkill = player.damage_data['Overkill'] / self.game_count
            self.streak = player.kill_streak['Peak']
            self.mitigated = player.crit_data['Mitigated'] / self.game_count
            self.crit_pct = player.crit_data['Ratio']
            self.parry_pct = player.crit_data['P_Ratio']
        else:
            self.kills = self.deaths = self.damage = self.effect = self.overkill = self.streak = self.mitigated = self.crit_pct = self.parry_pct = -1

    def print_kills_deaths(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
            f"Kills Per Game: {self.kills :.3f} (Avg {self.league_averages['Kills']})\n"
            f"Deaths Per Game: {self.deaths :.3f} (Avg {self.league_averages['Deaths']})\n\n")

    def print_effect(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Total Effect: {self.effect :.3f} (Avg {self.league_averages['Effect']})\n"
                    f"Overkill Effect: {self.overkill :.3f} (Avg {self.league_averages['Overkill']})\n\n")

    def print_streak(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Best Kill Streak: {self.streak}\n\n")

    def print_mitigated(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Damage Mitigated Per Game: {self.mitigated :.3f} (Avg {self.league_averages['Mitigated']})\n\n")

    def print_damage(self):
        with open('best_stats', 'a') as p:
            p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n"
                    f"Damage Dealt Per Game: {self.damage :.3f} (Avg {self.league_averages['Damage']})\n\n")

    def print_player_season(self, filename=None):


        if not filename:
            print(f"{self.player.name} (for S{self.season}_{self.player.team}),", end='')
            print(self.player.drafted + f" (this is their {ordinal_string(self.age )} season).")
            if self.sub_season:
                print(f"({self.sub_season})\n")
            else:
                print('\n')

            if self.season_grade_data != 0:
                print(f"Season Grade: {round(self.season_grade_data, 3)}\n")

            #print(f"Breakdown: {self.grade_breakdown}\n\n"
            print(f"Games Played: {self.player.games_played['This-Season']} ({self.match_count} matches)\n"
            f"Kills Per Game: {self.kills :.3f}\n"
            f"Deaths Per Game: {self.deaths :.3f}\n"
            f"Damage Dealt Per Game: {self.damage :.3f}\n"
            f"Damage Mitigated Per Game: {self.mitigated :.3f}\n"
            f"Total Effect Per Game: {self.effect :.3f}\n"
            f"Overkill Effect Per Game: {self.overkill :.3f}\n"
            f"Best Kill Streak: {self.streak}\n\n")
        else:
            with open(filename, 'a') as p:
                p.write(f"{self.player.name} (for S{self.season}_{self.player.team})\n")
                p.write(self.player.drafted + f" (this is their {ordinal_string(self.age)} season)." + '\n')
                if self.sub_season:
                    p.write(f"({self.sub_season})\n")
                if self.season_grade_data != 0:
                    p.write(f"Season Grade: {round(self.season_grade_data, 3)}\n")
                #p.write(f"Breakdown: {self.grade_breakdown}\n\n")
                p.write(f"Games Played: {self.player.games_played['This-Season']} ({self.match_count} matches)\n"
                f"Kills Per Game: {self.kills :.3f} (Avg {self.league_averages['Kills']})\n"
                f"Deaths Per Game: {self.deaths :.3f} (Avg {self.league_averages['Deaths']})\n"
                f"Damage Dealt Per Game: {self.damage :.3f} (Avg {self.league_averages['Damage']})\n"
                f"Damage Mitigated Per Game: {self.mitigated :.3f} (Avg {self.league_averages['Mitigated']})\n"
                f"Total Effect Per Game: {self.effect :.3f} (Avg {self.league_averages['Effect']})\n"
                f"Overkill Effect Per Game: {self.overkill :.3f} (Avg {self.league_averages['Overkill']})\n"
                f"Best Kill Streak: {self.streak}\n\n")

class Player:
    def __init__(self, tier, atk_dmg, atk_spd, crit_pct, crit_x, health, power, spawn_time, crit_dmg, name, team="None"):
        #baseline stats
        self.tier = tier
        self.atk_dmg = atk_dmg
        self.atk_spd = atk_spd
        self.crit_pct = crit_pct
        self.crit_x = crit_x
        self.overkill_x = 3
        self.max_health = health #redundant
        self.health = health
        self.power = power
        self.spawn_time = spawn_time
        self.drafted = "Not Drafted (Intro)"
        self.game_length = -1

        #in-game and in-season stats
        self.delayed_atk = 0
        self.is_alive = True
        self.countdown = 0
        self.kills = 0
        self.crit_kills = 0
        self.deaths = 0
        self.age = 0
        self.name = name
        self.crit_dmg = crit_dmg
        self.crit_data = {'Hit' : 0, 'Miss' : 0, 'Ratio' : 0.0, 'Parry' : 0, 'P_Miss' : 0, "P_Ratio" : 0.0, "Mitigated" : 0.0}
        self.grade_data = 0
        self.grade_dict = {'Power' : 0, 'Attack Damage' : 0, 'Attack Speed' : 0,'Critical-X' : 0, 'Critical-PCT' : 0, 'Health' : 0, 'Spawn' : 0, 'Kills' : 0, 'Deaths' : 0, 'Effect' : 0, 'Overkill' : 0, 'Mitigated' : 0, 'Damage' : 0, 'Rank' : -1}
        self.ratio = -1
        self.team = team
        self.dps = self.atk_dmg / self.atk_spd
        self.no_power = 0
        self.kill_streak = {'Current' : 0, 'Peak' : 0}
        self.damage_data = {'Tesseract' : 0.0, 'Total-Attacks' : 0, 'Total-Damage' : 0.0, 'Total-Delayed-Damage' : 0.0, 'Total-Delayed-X' : 0.0, 'Delayed-Count' : 0, 'Avg-Delayed-X' : 0.0, 'Avg-Delayed-Damage' : 0.0, 'Overkill' : 0.0, 'Overkill-Count' : 0}
        self.games_played = {'All' : 0, 'This-Season' : 0, 'Playoffs' : 0, 'Matches' : 0}
        self.game_stats = []

        self.xWAR = 0
        self.breakout = False

        self.trait_tag = None #Can equal Nuclear, Healer, Clutch, Butler, or Reflector

    def __str__(self):
        if self.deaths != 0:
            self.ratio = round((self.kills/self.deaths),4)
        x_breakdown = ""

        for word in ['Power', 'Attack Damage', 'Attack Speed', 'Critical-X', 'Critical-PCT', 'Health', 'Spawn']:
            x_breakdown += f"{word}({self.grade_dict[word]}), "
        if self.kills != 0:

            holder = f"{self.name}\n" \
            f"\t{self.team}\n"\
            f"xWAR: {self.xWAR} (Rank {self.grade_dict['Rank']})\n" \
                     f"{x_breakdown}\n" \
            f"Attack Damage: {self.atk_dmg}\n" \
            f"Attack Speed: {self.atk_spd}\n" \
            f"Crit %: {self.crit_pct}\n" \
            f"Crit X: {self.crit_x}\n" \
            f"Health: {self.max_health}\n" \
            f"Power: {self.power}\n" \
            f"Spawn Time: {self.spawn_time}\n" \
            f"AGE: {self.age}\n" \
            f"KILLS: {self.kills}\n" \
            f"DEATHS: {self.deaths}\n" \
            f"RATIO: {self.ratio}\n" \
            f"CRITICAL HIT KILLS: {self.crit_kills}\n" \
            f"NON-CRIT KILLS: {self.kills-self.crit_kills}\n"
        else:
            holder = f"{self.name}\n" \
            f"\t{self.team}\n" \
            f"xWAR: {self.xWAR} (Rank {self.grade_dict['Rank']})\n" \
            f"{x_breakdown}\n" \
            f"Attack Damage: {self.atk_dmg}\n" \
            f"Attack Speed: {self.atk_spd}\n" \
            f"Crit %: {self.crit_pct}\n" \
            f"Crit X: {self.crit_x}\n" \
            f"Health: {self.max_health}\n" \
            f"Power: {self.power}\n" \
            f"Spawn Time: {self.spawn_time}\n" \
            f"AGE: {self.age}\n"
        return holder

    def attack(self, defender):
        self.damage_data['Total-Attacks'] += 1
        damage = self.atk_dmg * (1 + self.delayed_atk)
        if self.delayed_atk > 0:
            self.damage_data['Total-Delayed-Damage'] += damage
            self.damage_data['Total-Delayed-X'] += self.delayed_atk
            self.damage_data['Delayed-Count'] += 1
        crit = False
        crit_roll = uniform(0, 1)
        if crit_roll <= self.crit_pct:
            damage *= self.crit_x
            crit = True
            if self.crit_data:
                self.crit_data['Hit'] += 1
        else:
            if self.crit_data:
                self.crit_data['Miss'] += 1

        parry_roll = uniform(0,1)
        if parry_roll <= defender.crit_pct:
            if defender.crit_data:
                defender.crit_data['Parry'] += 1
                defender.crit_data['Mitigated'] += damage
            damage = 0

        else:
            if defender.crit_data:
                defender.crit_data['P_Miss'] += 1
        defender.health -= damage
        self.damage_data['Total-Damage'] += damage
        if defender.health <= 0:
            defender.die()
            self.damage_data['Overkill'] += abs(3 * defender.health)
            self.damage_data['Overkill-Count'] += 1
            defender.deaths += 1
            if crit:
                self.crit_kills += 1
            self.kills += 1
            self.kill_streak['Current'] += 1
            self.delayed_atk = 0
            return True
        else:
            self.delayed_atk = 0
            return False

    def die(self):
        self.no_power += 1
        self.is_alive = False
        self.countdown = self.spawn_time
        if self.kill_streak['Current'] >= self.kill_streak['Peak']:
            self.kill_streak['Peak'] = self.kill_streak['Current']
        self.kill_streak['Current'] = 0

    def tesseract(self):
        self.damage_data['Tesseract'] += self.power
        return self.power

    def respawn(self):
        self.health = self.max_health
        self.is_alive = True

