from Games import best_of, enablePrint, blockPrint
from contests import round_robin, chain
from Player_Creator import s_tier, a_tier, b_tier, c_tier
from random import choice, randint, uniform, choices
from colorama import Fore, Back
# from dump_pickle import dump_pkl
from load_pickle import load_pkl, season_wipe
from numpy import mean
from Players import calculate_standard_deviation, PlayerSeason, grade_seasons
from stat_functions import region_mvp
from time import sleep
import pandas as pd
import math

def weighted_averages(team, season_no=-1):  # takes in a team and calculates weighted average of each stat, returns a dataframe
    #despite being called weighted_averages, this produces a full dataframe for a team season
    #todo add a function to this which extracts part of a team's history that shows how their season ended
    # could potentially add sub-function which quantifies how good a season is based on its finish, which could be
    # useful for tracing team stats to success

    final_dict = {'Team': team.name, 'Season' : season_no, 'Power': None, 'Attack Damage': None, 'Attack Speed': None, 'Critical %': None,
                  'Critical X': None, 'Health': None, 'Spawn Time': 0, 'Lineup Wins': team.wins,
                  'Lineup Losses': team.losses, 'Match Wins': team.match_wins, 'Match Losses': team.match_losses,
                  'Match Draws': team.match_draws}

    power_list = [player.power for player in team.players]
    total_power = (power_list[0] * 9) + (power_list[1] * 7) + (power_list[2] * 6) + (power_list[3] * 6) + (
                power_list[4] * 4) + (power_list[5] * 4)
    final_dict['Power'] = round((total_power / 36), 2)

    atk_dmg_list = [player.atk_dmg for player in team.players]
    total_atk_dmg = (atk_dmg_list[0] * 9) + (atk_dmg_list[1] * 7) + (atk_dmg_list[2] * 6) + (atk_dmg_list[3] * 6) + (
                atk_dmg_list[4] * 4) + (atk_dmg_list[5] * 4)
    final_dict['Attack Damage'] = round((total_atk_dmg / 36), 2)

    atk_spd_list = [player.atk_spd for player in team.players]
    total_atk_spd = (atk_spd_list[0] * 9) + (atk_spd_list[1] * 7) + (atk_spd_list[2] * 6) + (atk_spd_list[3] * 6) + (
                atk_spd_list[4] * 4) + (atk_spd_list[5] * 4)
    final_dict['Attack Speed'] = round((total_atk_spd / 36), 2)

    crit_pct_list = [player.crit_pct for player in team.players]
    total_crit_pct = (crit_pct_list[0] * 9) + (crit_pct_list[1] * 7) + (crit_pct_list[2] * 6) + (
                crit_pct_list[3] * 6) + (crit_pct_list[4] * 4) + (crit_pct_list[5] * 4)
    final_dict['Critical %'] = round((total_crit_pct / 36), 5)

    crit_x_list = [player.crit_x for player in team.players]
    total_crit_x = (crit_x_list[0] * 9) + (crit_x_list[1] * 7) + (crit_x_list[2] * 6) + (crit_x_list[3] * 6) + (
                crit_x_list[4] * 4) + (crit_x_list[5] * 4)
    final_dict['Critical X'] = round((total_crit_x / 36), 3)

    health_list = [player.max_health for player in team.players]
    total_health = (health_list[0] * 9) + (health_list[1] * 7) + (health_list[2] * 6) + (health_list[3] * 6) + (
                health_list[4] * 4) + (health_list[5] * 4)
    final_dict['Health'] = round((total_health / 36), 3)

    spawn_list = [player.spawn_time for player in team.players]
    total_spawn = (spawn_list[0] * 9) + (spawn_list[1] * 7) + (spawn_list[2] * 6) + (spawn_list[3] * 6) + (
                spawn_list[4] * 4) + (spawn_list[5] * 4)
    final_dict['Spawn Time'] = round((total_spawn / 36), 2)

    return pd.DataFrame([final_dict])

def team_season_dataframe(teams, season_no = -1):
    #writes the average team player innate stats and their season record to a file
    #despite the name, this takes in a list of teams and writes them out after making a DF

    team_stats_df = pd.DataFrame(columns=['Team', 'Season', 'Power', 'Attack Damage', 'Attack Speed', 'Critical %', 'Critical X',
                                              'Health', 'Spawn Time', 'Lineup Wins', 'Lineup Losses',
                                              'Match Wins', 'Match Losses', 'Match Draws'])

    path = "C:/Users/carte/OneDrive/Documents/ControlAverageStats.xlsx"
    team_stats_df = pd.read_excel(path)

    try:
        team_names = list(team_stats_df['Team'])
    except KeyError:
        team_names = list(['None'])
        team_stats_df = pd.DataFrame(
            columns=['Team', 'Season', 'Power', 'Attack Damage', 'Attack Speed', 'Critical %', 'Critical X',
                     'Health', 'Spawn Time', 'Lineup Wins', 'Lineup Losses',
                     'Match Wins', 'Match Losses', 'Match Draws'])

    for team in teams:
        # Check if the team's name and season_no combination exists in the DataFrame
        if not ((team_stats_df['Team'] == team.name) & (team_stats_df['Season'] == season_no)).any():
            # Append the team's data for the given season to the DataFrame
            team_stats_df = pd.concat([team_stats_df, weighted_averages(team, season_no)])

    with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        team_stats_df.to_excel(writer, sheet_name='TeamWeightedAverages', index=False)



#this will allow me to manually draft players for each team

def write_champ(champ, season_count, region, champ_list=None):
    #the champ list from main is a dictionary with keys for seasons, and values as a nested dictionary with each region's name as a key and the champ as a value
    #this function will be run with only a single season's dictionary of champions, with the season_count imported separately
    valid_regions = ['Darkwing Regional', 'Shining-Core Regional', 'Diamond-Sea Regional',
                     'Web-of-Nations Regional', 'Ice-Wall Regional', 'Candyland Regional', "Hell's-Circle Regional",
                     'Steel-Heart Regional']
    with open("champs", 'a') as c:
        if region in valid_regions:
            c.write(f"S{season_count} {region} Champion: {champ.name}\n"
                    f"Entered playoffs as the {champ.seed} seed.\n\n")
        else:
            c.write(f"S{season_count} Universal Champion: {champ.name}\n"
                    f"Entered playoffs as the {champ.seed} seed.\n\n")

def ordinal_string(n: int) -> str:
    if 10 <= n % 100 < 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
def half_to_one(num):
    x = (abs(num - 1)) / 2
    return (num + x) if num < 1 else (num - x)

def grade_players(players, is_team=None):
    #should take in a list of players, not a dict draft class

    #xWAR coefficient changes
    # .001 Critical Chance (+26.40 / -29.83) has impacted ratings far too much. It's being dropped to +1.20 / -1.25
    # .1 Critical Multiplier (+0.79 / -16.26) the negative coefficient has ruined the game. It is being slashed
    # all the way down to 0.91
    # 1 Attack Damage (+16.67 / -15.83) is being slightly increased to impact the game more to 18.50 / -18.00
    # -1 Power is being adjusted from -320.01 to -305.99 to be closer to the positive coefficient.
    # +1 Spawn Time is being adjusted from -149.98 to 114.42 to be closer to the negative coefficient
    # 1 Power (+293.01 / -305.99) is being scaled down to match other variables dropping; now 250 / -260

    pos_xWAR_coefficient = {'1 Attack Speed' : -81.46, '1 Attack Damage' : 18.50, '1 Health' : 0.34,
                            '1 Power' : 250, '1 Spawn Time' : -104.42, '.001 Critical Chance' : 1.2,
                            '.1 Critical Multiplier' : 0.79}
    #positive coefficient is multiplied by (player_stat - average_stat) if player_stat > average_stat

    neg_xWAR_coefficient = {'1 Attack Speed' : 73.92, '1 Attack Damage' : -18.00, '1 Health' : -1.44,
                            '1 Power' : -260, '1 Spawn Time' : 100.78, '.001 Critical Chance' : -1.25,
                            '.1 Critical Multiplier' : -0.91}
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

    avg_kills = mean([player.kills for player in players])
    avg_deaths = mean([player.deaths for player in players])
    avg_damage = mean([player.damage_data['Total-Damage'] for player in players])
    avg_effect = mean([player.damage_data['Tesseract'] for player in players])
    avg_overkill = mean([player.damage_data['Overkill'] for player in players])
    avg_mitigated = mean([player.crit_data['Mitigated'] for player in players])




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



def user_draft(teams, season_count, is_regional=False, void=False, second = False,
               draft_name='Default', league_season_stats= None, auto_mine = True, third = False):

    #league_season_stats will import the season stats from the league in which the draft is being held,
    #so that I can import it into grade_player_seasons to grade the seasons of my players in relation to
    #the rest of the league they are in

    from random import uniform
    number = -1
    with open('draft_history', 'w') as bruh:
        bruh.write('')
    draft_class = {}
    if not is_regional and not void: #universal draft
        for i in [0,1]:
            add = s_tier(round(uniform(2,6),2))
            add.team = i
            draft_class[i] = add
        for i in [2,3,4,5,6,7,8]:
            add = a_tier(round(uniform(2,5),2))
            add.team = i
            draft_class[i] = add
        for i in [9,28,29]:
            add = a_tier(randint(3,5))
            add.team = i
            draft_class[i] = add
        for i in [10,11,12,13,14,15,16]:
            add = b_tier(round(uniform(2,5.5),2))
            add.team = i
            draft_class[i] = add
        for i in [17,30]:
            add = b_tier(randint(3,6))
            add.team = i
            draft_class[i] = add
        for i in [18,19,20,21,22,23,25,26,27]:
            add = c_tier(round(uniform(2,7),2))
            add.team = i
            draft_class[i] = add
        for i in [24]:
            add = c_tier(randint(1,8))
            add.team = i
            draft_class[i] = add
    elif is_regional and not void: #regional draft
        for i in [25,26,27,28,29,30]:
            add = s_tier(round(uniform(1,5),1))
            add.team = i
            draft_class[i] = add
        for i in [0,1,2,3,4,5,6]:
            add = a_tier(round(uniform(1,6),2))
            add.team = i
            draft_class[i] = add
        for i in [10,11,12,13,14,15,16,17,18,19,20]:
            add = b_tier(round(uniform(1,6),2))
            add.team = i
            draft_class[i] = add
        for i in [21,22,23,24,7,8,9]:
            add = c_tier(round(uniform(1,7),2))
            add.team = i
            draft_class[i] = add
    elif void:
        for i in range(len(teams)):
            if i%2 == 0:
                add = b_tier(round(randint(10000,60000)/10000, 2))
            else:
                add = a_tier(round(randint(10000,60000)/10000, 2))
            add.team = i
            draft_class[i] = add
        for i in range(6):
            add = s_tier(round(randint(10000,60000)/10000, 2))
            add.team = i
            draft_class[i] = add
    if second:
        #104 teams miss regional playoffs (second_pick == 1)
        # up to 64 teams (but never close to 64) could be second_pick == 2
        # so draft_class should be 104 good players and 64 decent players
        # secondary draft will also run grade_players on all team rosters and the draft class
        # so that teams can see if there is a player remaining in the draft that is better than their worst player
        #if there is no option for upgrade, they pass the pick

        second_all_players = []
        base = len(teams)

        for i in range((base-10)):
            if i%3 == 0:
                add = s_tier(round(uniform(2.0,4.5), 2))
            elif i%3 == 1:
                add = a_tier(round(uniform(2.5, 4.0), 2))
            else:
                add = b_tier(round(uniform(1.5, 5.0), 2))
            add.team = i
            draft_class[i] = add
        for i in range((base-10), (base+25)):
            if i%3 == 0:
                add = a_tier(round(uniform(1.0,5.0), 2))
            elif i%3 == 1:
                add = b_tier(round(uniform(0.5, 5.5), 2))
            else:
                add = c_tier(round(uniform(2.0, 6.5), 2))
            add.team = i
            draft_class[i] = add
        for i in [(base+26), (base+27), (base+28)]:
            add = a_tier(6.25)
            add.team = i
            draft_class[i] = add

        for team in teams:
            team.second_pick = 0
            for player in team.players:
                second_all_players.append(player)
    elif third:
        third_all_players = []

        for team in teams:
            team.second_pick = 0
            for player in team.players:
                third_all_players.append(player)

        base = len(teams) + 18
        for i in range(base):
            if i%4 == 0:
                coin = choice([True, False])
                if coin:
                    add = s_tier(round(uniform(3.0,6.0), 2))
                else:
                    add = c_tier(round(uniform(2.0,7.0), 2))
            if i%4 == 1:
                coin = choice([True, False, False])
                if coin:
                    add = s_tier(round(uniform(3.0, 6.0), 2))
                else:
                    add = b_tier(round(uniform(1.5, 5.5), 2))
            if i%4 == 2:
                coin = choice([True, False, False, False])
                if coin:
                    add = s_tier(round(uniform(3.0, 6.0), 2))
                else:
                    add = a_tier(round(uniform(2.0, 5.0), 2))
            if i%4 == 3:
                coin = choice([True, False, False, False, False])
                if coin:
                    add = s_tier(round(uniform(3.5, 6.5), 2))
                else:
                    add = s_tier(round(uniform(1.0, 5.0), 2))
            #ignore error
            add.team = i
            draft_class[i] = add


    p = draft_class.copy()
    if second:
        #ignore
        temp_players = list(p.values()) + second_all_players
        grade_players(list(temp_players))
    elif third:
        #ignore
        temp_players = list(p.values()) + third_all_players
        grade_players(list(temp_players))
    else:
        grade_players(list(p.values()))

    #if it is a second round, grade_players will assign player.grade_dict['Rank'] to all players
    #they are ranked in a list which contains all players from all teams with a Second Round draft pick, and
    #all the players in the Second Round draft class
    #teams will select another player only if there is a player on the draft list with a better rank than
    #their lowest ranked player. and, of course, they will pick the highest ranked player in the draft class
    p = dict(sorted(p.items(), key=lambda plyr: plyr[1].xWAR, reverse=True))

    for i in range(len(teams)):
        with open('draft_list', 'w', buffering=10) as f:
            f.write(f"{draft_name}")
        with open('draft_list', 'a', buffering=10) as f:

            f.write(f" {len(p.values())} of {len(draft_class)} players remaining.\n")
            for player in p.values():
                f.write('\n')
                f.write('\n')
                f.write(str(player))
                f.write('\n')

        with open('draft_history', 'a') as x:
            x.write(f"{i+1}. {teams[i].name} to select.\n")
        grade_players(teams[i].players)
        if teams[i].mine and not auto_mine: # make sure to keep auto_mine on because this has not been updated to work
            enablePrint()
            x=0
            my_players_seasons = []
            if league_season_stats:
                full_season_list = []
                for val in league_season_stats.values():
                    for season in val:
                        full_season_list.append(season)


                for player in teams[i].players:
                    temp = PlayerSeason(player, season_count)
                    my_players_seasons.append(temp)
                grade_seasons(my_players_seasons, True, import_averages=full_season_list)
                my_players_seasons.sort(key=lambda szn : szn.season_grade_data, reverse=True)
                for thing in my_players_seasons:
                    thing.print_player_season(filename='my_teams')
                    print(f"({x})")
                    thing.print_player_season()
                    x+=1
            else:
                for player in teams[i].players:
                    temp = PlayerSeason(player, season_count)
                    temp.print_player_season(filename='my_teams')
                    print(f"({x})")
                    temp.print_player_season()
                    x += 1
            print(f"{teams[i].name} to select.")
            try:
                terminate = int(input("Choose player index to terminate."))
            except IndexError:
                terminate = int(input("Choose 0, 1, 2, or 3."))
            index = int(input("Choose player index to draft."))
            try:
                draft(p[index], teams[i], index=i, season_count=season_count, void=void, repl=terminate)
            except KeyError:
                print("Index unavailable. Options are:",end=' ')
                for key in p.keys():
                    print(key,end=', ')
                print('')
                index = int(input("Choose player index to draft."))
                draft(p[index], teams[i], index=i, season_count=season_count, void=void, repl=terminate)
            del p[index]
        else:
            players_in_class = list(p.values())

            top_player = s_tier()
            top_player.grade_dict['Rank'] = 1000

            for player in players_in_class:
                if player.grade_dict['Rank'] < top_player.grade_dict['Rank']:
                    top_player = player

            index = top_player.team

            teams[i].players.sort(key=lambda pl: pl.xWAR, reverse=True)
            if second:
                if teams[i].players[5].xWAR < top_player.xWAR:
                    draft(p[index], teams[i], index=i, season_count=season_count, void=void, second=True)
                    del p[index]
                else:
                    teams[i].history[season_count] += f"\tPassed Secondary pick.\n"
            elif third:
                if teams[i].players[5].xWAR < top_player.xWAR:
                    try:
                        draft(p[index], teams[i], index=i, season_count=season_count, void=void, third=True)
                        del p[index]
                    except KeyError:
                        pass
                else:
                    teams[i].history[season_count] += f"\tPassed Tertiary pick.\n"
            else:
                draft(p[index], teams[i], index=i, season_count=season_count, void=void)
                del p[index]


def draft(player, team, index, season_count, repl=5, void=False, second=False, third=False):
    if void:
        team.region = 'Void'
    # team.print_roster()
    old = team.players[repl]
    team.players[repl] = player
    player.team = team.name
    if second:
        player.drafted = f"Drafted {ordinal_string(index + 1)} in the S{season_count} Second Round draft"
        team.history[season_count] += f"\tWith the {ordinal_string(index + 1)} pick in the Second Round draft, selected {player.name}" \
                                      f" (Terminated {old.name})\n"
        team.second_pick = 0
    elif third:
        player.drafted = f"Drafted {ordinal_string(index + 1)} in the S{season_count} Third Round draft"
        team.history[
            season_count] += f"\tWith the {ordinal_string(index + 1)} pick in the Third Round draft, selected {player.name}" \
                             f" (Terminated {old.name})\n"
        team.second_pick = 0
    else:
        player.drafted = f"Drafted {ordinal_string(index+1)} in the S{season_count} {team.region} draft"
        team.history[season_count] += f"\n\tWith the {ordinal_string(index+1)} pick in the {team.region} draft, selected {player.name}" \
                                      f" (Terminated {old.name})\n"
    with open('draft_history', 'a') as x:
        x.write(f"{player.name} has been drafted to {team.name}\n{old.name} terminated.\n")

def player_changes(teams, season_count=-1):
        def level_out(pl):
            level_age_factor = 1 - ((pl.age + 3) / 100)
            list_of_100 = [num for num in range(100)]

            if pl.power > 62:
                pl.power = 62
            if pl.atk_spd < 6:
                pl.atk_spd = 6
            while pl.atk_dmg >= 77:
                pl.atk_dmg = round(pl.atk_dmg * level_age_factor)
            while pl.max_health >= 999:
                pl.max_health = round((pl.max_health * level_age_factor), 2)
                if choice(list_of_100) == 50:
                    pl.max_health -= 120
            while pl.crit_x >= 14.00:
                pl.crit_x = round((pl.crit_x * level_age_factor), 3)
                if choice(list_of_100) == 50:
                    pl.crit_x -= 3
            while pl.crit_pct >= 0.1:
                pl.crit_pct = round((pl.crit_pct * level_age_factor), 4)
                if choice(list_of_100) == 50:
                    pl.crit_pct -= 0.025

        for team in teams:
            for player in team.players:
                breakout_coin = randint(1,200)
                if breakout_coin == 100:
                    x_factor = choice([0.25, 0.3, 0.35])
                    team.history[season_count] += f"\n\tLOTTERY: {player.name} will have a breakout season!\n"
                elif player.breakout:
                    x_factor = choice([0.2, 0.25, 0.3, 0.3, 0.35, 0.4])
                else:
                    x_factor = 0

                age_factor = [1.25, 1.2, 1.1, 1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45]
                for _ in range(5):
                    age_factor.append(.437)
                for i in range(500):
                    age_factor.append((.435 - (i/1000)))
                tier_factor = {'S' : choice([-0.05, -0.025, -0.02, 0, 0.01]), 'A' : choice([0.02, -0.01, -0.01]), 'B' : choice([0.01, 0.01, -0.03]), 'C' : 0.05}
                t_factor = tier_factor[player.tier]*half_to_one(age_factor[player.age])
                factor = age_factor[player.age] + t_factor + x_factor
                coin = choice([True,False])
                if coin:
                    player.atk_dmg = round(player.atk_dmg * factor)
                    player.max_health = round(player.max_health * factor, 2)
                else:
                    player.crit_pct = round(player.crit_pct * factor, 4)
                    player.crit_x = round(player.crit_x*factor, 3)
                power_coin = uniform(0,2)
                if factor > power_coin:
                    p2_coin = choice([0,1,1,2])
                    player.power += p2_coin
                else:
                    p2_coin = choice([0, -1, -1, -1, -2])
                    player.power += p2_coin


                player.crit_dmg = player.crit_x * player.atk_dmg
                level_out(player)

def double_elim_16(t, r1_thresh=55, r2_thresh=70, r3_thresh=90, r4_thresh=125, final_thresh=160, is_relegation=False, upset_list = None, upset_count = None, region = 'Universal'):

    out1 = [0,0,0,0]
    out2 = [0,0,0,0]
    out3 = [0,0]
    out4 = [0,0]

    def transform_list(numbers):
        transformed_numbers = [round(num * 0.35) for num in numbers]
        return transformed_numbers

    if is_relegation:
        r1_thresh, r2_thresh, r3_thresh, r4_thresh, final_thresh = transform_list([r1_thresh, r2_thresh, r3_thresh, r4_thresh, final_thresh])

    m1,m2,m3,m4,mF,mGF = round(r1_thresh/6)+11, round(r2_thresh/7)+7, round(r3_thresh/7)+5, round(r4_thresh/9)+9, round(final_thresh/10)+10, round(final_thresh/10)+21

    one, two, three, four, five, six, seven, eight = t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]
    nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen = t[8], t[9], t[10], t[11], t[12], t[13], t[14], t[15]
    if is_relegation:
        one.seed, two.seed, three.seed, four.seed, five.seed, six.seed, seven.seed, eight.seed, nine.seed, ten.seed, eleven.seed, twelve.seed, thirteen.seed, fourteen.seed, fifteen.seed, sixteen.seed = 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
        print(Fore.RED + "RELEGATION TOURNAMENT" + Fore.RESET)
    else:
        one.seed, two.seed, three.seed, four.seed, five.seed, six.seed, seven.seed, eight.seed, nine.seed, ten.seed, eleven.seed, twelve.seed, thirteen.seed, fourteen.seed, fifteen.seed, sixteen.seed = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
        print(Fore.RED + "UNIVERSAL PLAYOFFS" + Fore.RESET)
    print(Fore.GREEN + "R1 winner bracket" + Fore.RESET)
    context = f"R1W {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w1, l1 = best_of(one, sixteen, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w2, l2 = best_of(eight, nine, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w3, l3 = best_of(five, twelve, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w4, l4 = best_of(four, thirteen, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w5, l5 = best_of(three, fourteen, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w6, l6 = best_of(six, eleven, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w7, l7 = best_of(seven, ten, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w8, l8 = best_of(two, fifteen, r1_thresh,10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R1 loser bracket" + Fore.RESET)
    context = f"R1L {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w9, out1[0] = best_of(l1, l2, r1_thresh, 10, True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w10, out1[1] = best_of(l3, l4, r1_thresh, 10,True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w11, out1[2] = best_of(l5, l6, r1_thresh, 10, True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w12, out1[3] = best_of(l7, l8, r1_thresh, 10, True,m1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R2 winner bracket" + Fore.RESET)
    context = f"R2W {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w13, l13 = best_of(w1, w2, r2_thresh, 11, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w14, l14 = best_of(w3, w4, r2_thresh, 11, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w15, l15 = best_of(w5, w6, r2_thresh, 11, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w16, l16 = best_of(w7, w8, r2_thresh, 11, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R2 loser bracket" + Fore.RESET)
    context = f"R2L {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w17, out2[0] = best_of(w9, l16, r2_thresh, 10, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w18, out2[1] = best_of(w10, l15, r2_thresh, 10, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w19, out2[2] = best_of(w11, l14, r2_thresh, 10, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w20, out2[3] = best_of(w12, l13, r2_thresh, 10, True,m2,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R3 winner bracket" + Fore.RESET)
    context = f"R3W {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w21, l21 = best_of(w13, w14, r3_thresh, 12, True,m3,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w22, l22 = best_of(w15, w16, r3_thresh, 12, True,m3,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R3 loser bracket" + Fore.RESET)
    context = f"R3L {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w23, out3[0] = best_of(w17, w18, r3_thresh, 10, True,m3,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w24, out3[1] = best_of(w19, w20, r3_thresh, 10, True,m3,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R4 loser bracket" + Fore.RESET)
    context = f"R4L {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w25, out4[0] = best_of(w23, l21, r4_thresh, 10, True,m4,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    w26, out4[1] = best_of(w24, l22, r4_thresh, 10, True,m4,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "winner bracket finals" + Fore.RESET)
    context = f"WB Finals {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w27, l27 = best_of(w21, w22, r4_thresh, 13, True,mF,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "loser bracket finals" + Fore.RESET)
    context = f"LB Finals {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w28, out5 = best_of(w25, w26, r4_thresh, 10, True,mF,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "winner bracket finals LOSER vs loser bracket champ" + Fore.RESET)
    context = f"WBFL v LBC {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w29, out6 = best_of(w28, l27, r4_thresh, 13, True,mF,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "grand finals" + Fore.RESET)
    context = f"Grand Finals {region} "
    if is_relegation:
        context += "Relegation Tournament"
    else:
        context += "Playoffs"
    w30, out7 = best_of(w27, w29, final_thresh, 14, True,mGF,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
    if w30 == w27:
        print(Fore.GREEN + f"{w30.full_name} are flawless." + Fore.RESET)
        champ = w30
    else:
        print(Fore.GREEN + f"{w27.full_name} has only lost once. {w29.full_name} must win again." + Fore.RESET)
        w31, out7 = best_of(w27, w29, final_thresh, 14, True,mGF+1,test_output=True,is_uni=not is_relegation,upset_list=upset_list,upset_count=upset_count,context=context)
        champ = w31
    out1.sort(key = lambda t : t.seed)
    out2.sort(key=lambda t: t.seed)
    out3.sort(key=lambda t: t.seed)
    out4.sort(key=lambda t: t.seed)
    return champ, out7, out6, out5, out4[0], out4[1], out3[0], out3[1], out2[0], out2[1], out2[2], out2[3], out1[0], out1[1], out1[2], out1[3]


def double_elim_8(t,r1_thresh=75, r2_thresh=85, r3_thresh=100, r4_thresh=150, final_thresh=200, upset_list = None, upset_count = None, region = None):
    out_1 = []
    out_2 = []

    r1_margin, r2_margin, r3_margin, r4_margin, final_margin = round(r1_thresh/5)+5, round(r2_thresh/5)+5, round(r3_thresh/5)+5, round(r4_thresh/5)+5, round(final_thresh/5)+1

    one, two, three, four, five, six, seven, eight = t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7]
    one.seed, two.seed, three.seed, four.seed, five.seed, six.seed, seven.seed, eight.seed = 1, 2, 3, 4, 5, 6, 7, 8
    print(Fore.GREEN + "R1 winner bracket" + Fore.RESET)
    context = f"R1W {region} Playoffs"
    w1, l1 = best_of(one, eight, r1_thresh,3, True,r1_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    w2, l2 = best_of(four, five, r1_thresh,3,True,r1_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    w3, l3 = best_of(three, six, r1_thresh,3,True,r1_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    w4, l4 = best_of(two, seven, r1_thresh,3,True,r1_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R1 loser bracket" + Fore.RESET)
    context = f"R1L {region} Playoffs"
    w5, out_temp = best_of(l1, l2, r1_thresh, 3, True,r1_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    out_1.append(out_temp)
    w6, out_temp = best_of(l3, l4, r1_thresh, 3, True,r1_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    out_1.append(out_temp)
    print(Fore.GREEN + "R2 winner bracket" + Fore.RESET)
    context = f"R2W {region} Playoffs"
    w7, l7 = best_of(w1, w2, r2_thresh, 4, True,r2_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    w8, l8 = best_of(w3, w4, r2_thresh, 4, True,r2_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "R2 loser bracket" + Fore.RESET)
    context = f"R2L {region} Playoffs"
    w9, out_temp = best_of(w5, l8, r2_thresh, 4, True,r2_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    out_2.append(out_temp)
    w10, out_temp = best_of(w6, l7, r2_thresh, 4, True,r2_margin, upset_list=upset_list,upset_count=upset_count,context=context)
    out_2.append(out_temp)
    print(Fore.GREEN + "winner bracket finals" + Fore.RESET)
    context = f"WB Finals {region} Playoffs"
    w11, l11 = best_of(w7, w8, r3_thresh, 5, True,r3_margin,test_output=True, upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "loser bracket finals" + Fore.RESET)
    context = f"LB Finals {region} Playoffs"
    w12, out_final = best_of(w9, w10, r3_thresh, 5, True,r3_margin,test_output=True, upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "winner bracket finals LOSER vs loser bracket champ" + Fore.RESET)
    context = f"WBFL v LBC {region} Playoffs"
    w13, out_third = best_of(w12, l11, r4_thresh, 5, True,r4_margin,test_output=True, upset_list=upset_list,upset_count=upset_count,context=context)
    print(Fore.GREEN + "grand finals" + Fore.RESET)
    context = f"Grand Finals {region} Playoffs"
    w14 = best_of(w11, w13, final_thresh, 6, False,final_margin,test_output=True, upset_list=upset_list,upset_count=upset_count,context=context)
    if w14 == w11:
        print(Fore.GREEN + f"{w14.name} are flawless." + Fore.RESET)
        champ = w14
        runner_up = w13
    else:
        print(Fore.GREEN + f"{w11.name} has only lost once. {w13.full_name} must win again." + Fore.RESET)
        champ, runner_up = best_of(w11, w13, final_thresh, 6, True,final_margin+1,test_output=True, upset_list=upset_list,upset_count=upset_count,context=context)
    out_1.sort(key=lambda x: x.seed, reverse=False)
    out_2.sort(key=lambda x: x.seed, reverse=False)
    s = [out_1[1], out_1[0], out_2[1], out_2[0], out_final, out_third, runner_up, champ]
    return s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]

def swiss_format(teams, base_thresh, base_margin, win_thresh=3):
    advanced = []
    eliminated = []
    def round(wins, losses):
        print(Fore.RED + f"ROUND ({wins},{losses})" + Fore.RESET)
        while len(league_records[(wins,losses)]) >= 2:
            cont1 = choice(league_records[(wins, losses)])
            league_records[(wins, losses)].remove(cont1)
            cont2 = choice(league_records[(wins, losses)])
            winner, loser = best_of(cont1, cont2, base_thresh, amp=4, both_return=True, win_by=base_margin)
            league_records[(wins, losses)].remove(cont2)
            if wins+1 < win_thresh:
                league_records[(wins+1, losses)].append(winner)
            elif wins+1 == win_thresh:
                print(Fore.GREEN + f"{winner.name} advance." + Fore.RESET)
                advanced.append(winner)
            if losses+1 < win_thresh:
                league_records[(wins, losses+1)].append(loser)
            elif losses+1 == win_thresh:
                print(Fore.GREEN + f"{loser.name} are eliminated." + Fore.RESET)
                eliminated.append(loser)


    league_records = {} # keys = list which contains wins and losses
    # values are lists of teams which have that record
    for j in range(0,win_thresh):
        for i in range(0,win_thresh):
            league_records[(i,j)] = []
    league_records[(0, 0)] = teams.copy()
    for j in range(0,win_thresh):
        for i in range(0,win_thresh):
            round(i,j)

    return advanced, eliminated



def league_season(TEAMS,use_saved=False,season_count=-1,final_reversed=True,region='Universal', stats_list=None, upset_list = None, upset_count = None, champ_list=None):
    # the stats_list parameter will take in a dictionary with keys of season numbers and values of lists of
    #player seasons, with one object for each player in that league
    #after edits, this function will create a key in that dictionary corresponding to season_count
    #and a list value with all the players' REGULAR SEASON statistics as a value
    missed_playoffs = []
    play_in = []
    dumpster_fire = []

    if use_saved:
        TEAMS = load_pkl()
    if len(TEAMS) < 30:
        post_range = 10
        chain_range = None
    elif len(TEAMS) >= 30:
        post_range = 14
        chain_range = 16
    else:
        chain_range = None
        post_range = None
    # see scratch_paper notes on relegation chain
    sub_season = f"{region} Regular Season"



    if region == 'Universal':
        if chain_range:
            postseason, relegation_chain = round_robin(TEAMS, r=9, qualify_range=post_range, alt_qualify_range=chain_range)
        else:
            postseason = round_robin(TEAMS, 4, qualify_range=post_range)
            relegation_chain = None
    else:
        postseason = round_robin(TEAMS, 2, qualify_range=post_range)
        relegation_chain = None

    for team in TEAMS:

        if stats_list:
            for player in team.players:
                temp = PlayerSeason(player, season_count, sub_season=sub_season)
                stats_list[season_count].append(temp)
                #this loop will add the regular season stats of each player to their respective region's stat_list in main
                #the issue I am having right now is that these objects contain far more games than just the regular season
                #the regular season is only 126 games (6*21) but some of these objects contain over a thousand for certain iterations
                #I need to find where and when game_count['This Season'] is iterated for players, which is likely the root of the problem
                #ANS: season_wipe sets the values for each player to zero

        if team not in postseason:
            if chain_range:
                if team in relegation_chain:
                    team.history[season_count] += f" {ordinal_string(team.seed)} in Universal League -> Relegation Tournament."
                else:
                    team.history[season_count] += f" {ordinal_string(team.seed)} in Universal League -> S_{season_count+1} Universal Qualifying."
                    missed_playoffs.append(team)
            else:
                missed_playoffs.append(team)
                team.history[season_count] += f" {ordinal_string(team.seed)} in {region} League, missed playoffs."
                team.second_pick = 1
                if team.seed == 20 or team.seed == 21 or team.seed == 22:
                    dumpster_fire.append(team)

    if stats_list:
        region_mvp(stats_list, season_count, region)
    if post_range == 10:
        one, two, three, four, five, six = postseason[0], postseason[1], postseason[2], postseason[3], postseason[4],postseason[5]
        for i in [6,7,8,9]:
            play_in.append(postseason[i])
            postseason[i].third_pick = 1
        seven, p1 = best_of(play_in[0], play_in[1], 35, 8, True, 4,upset_list=upset_list,upset_count=upset_count,context=f"{region} Play-In")
        p2, tenth = best_of(play_in[2], play_in[3], 35, 8, True, 4,upset_list=upset_list,upset_count=upset_count,context=f"{region} Play-In")
        eight, ninth = best_of(p1, p2, 35, 8, True, 4,upset_list=upset_list,upset_count=upset_count,context=f"{region} Play-In")

        tenth.history[season_count] += f" Lost in {region} play-in, finished 10th."
        ninth.history[season_count] += f" Lost in {region} play-in, finished 9th."

        playoff_one = [one, two, three, four, five, six, seven, eight]

        eighth, seventh, sixth, fifth, fourth, third, second, champ = double_elim_8(
            playoff_one,upset_list=upset_list,upset_count=upset_count,region=region) if region == 'Universal' else double_elim_8(playoff_one, 45, 55, 65, 75, 90,upset_list=upset_list,upset_count=upset_count,region=region)



        for team in playoff_one:
            team.accolades['Regional-Playoffs'] += 1
        champ.accolades['Regional-Champ'] += 1
        relegation_standings = None
        playoff_standings = [champ, second, third, fourth, fifth, sixth, seventh, eighth]
    elif post_range == 16 or post_range == 14 or chain_range:
        relegation_standings = list(double_elim_16(relegation_chain, r1_thresh=170, r2_thresh=200, r3_thresh=225, r4_thresh=250, final_thresh=300, is_relegation=True,upset_list=upset_list,upset_count=upset_count,region=region))
    if chain_range:
        for i in [0,1]:
            relegation_standings[i].history[season_count] += f" {ordinal_string(i+15)} in Relegation Tournament -> UNI Playoffs."
            postseason.append(relegation_standings[i])
            print(Fore.BLUE + f"{relegation_standings[i].name} is going to the playoffs." + Fore.RESET)

        for i in [2,3,4,5]:
            relegation_standings[i].history[
                season_count] += f" {ordinal_string(i+15)} in Relegation Tournament -> S_{season_count+1} Universal League."
            missed_playoffs.insert(i-2, relegation_standings[i])
            print(Fore.BLUE + f"{relegation_standings[i].name} will remain in the Universal League." + Fore.RESET)

        for i in range(6,len(relegation_standings)):
            relegation_standings[i].history[
                season_count] += f" {ordinal_string(i+15)} in Relegation Tournament -> S_{season_count+1} Universal Qualifying."
            print(Fore.BLUE + f"{relegation_standings[i].name} is on the chopping block." + Fore.RESET)
            missed_playoffs.insert(i-2, relegation_standings[i])


        playoff_one = list(postseason)
        champ, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth = double_elim_16(postseason, 210, 270, 400, 500, 750,upset_list=upset_list,upset_count=upset_count,region=region)
        playoff_standings = [champ, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth]
        for team in playoff_one:
            team.accolades['Universal-Playoffs'] += 1
        champ.accolades['Universal-Champ'] += 1




    playoff_standings_alt = [second, third, fourth, fifth, sixth, seventh, eighth] if post_range == 10 else [second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth]
    place = 1
    for team in playoff_standings_alt:
        place+=1
        team.history[season_count] += f" {region} playoffs as {team.seed} seed, finished {ordinal_string(place)}."
    if region != 'Universal':
        champ.history[
            season_count] += f" {region} playoffs as {champ.seed} seed, WON CHAMPIONSHIP. -> UNI Qualifier."
        for team in [second, third, fourth, fifth]:
            team.history[season_count] += f" -> PQ Swiss."
        for team in [sixth, seventh, eighth, ninth]:
            team.history[season_count] += f" -> Last Stand Tournament."
    else:
        champ.history[season_count] += f" Universal playoffs as {champ.seed} seed, WON CHAMPIONSHIP."

    print(Fore.RED + f"{champ.name} have won the {region} League." + Fore.RESET)

    sleep(8 if region == "Universal" and season_count != 0 else 0.5)

    if ninth and tenth:
        play_in_standings = [ninth, tenth]
        final_standings = playoff_standings + play_in_standings + missed_playoffs
    else:
        final_standings = playoff_standings + missed_playoffs
    for team in final_standings:
        if team.mine:
            print(Fore.BLUE + f"{team.name}: {team.history[season_count]}"
                  + Fore.RESET)




    if champ_list:
        write_champ(champ, season_count, region, champ_list=champ_list)
    else:
        write_champ(champ, season_count, region)

    for pos in range(len(final_standings)):
        final_standings[pos].seed = pos

    if final_reversed:
        final_standings.reverse()
    for t in dumpster_fire:
        coin = choice([0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,3])
        unblessed = [0, 1, 2]
        if coin != 0:
            for _ in range(coin):
                blessed_index = choice(unblessed)
                t.players[blessed_index].breakout = True
                try:
                    unblessed.remove(blessed_index)
                except IndexError:
                    pass
                t.history[season_count] += f"\n\tBLESSING: {t.players[blessed_index].name}(Slot {blessed_index}) will have a breakout season!"

    team_season_dataframe(final_standings, season_no=season_count)

    if champ_list:
        return  final_standings, champ_list
    else:
        return final_standings

