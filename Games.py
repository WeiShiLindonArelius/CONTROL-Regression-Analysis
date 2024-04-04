from random import randint, choice, seed
from stat_functions import series_test
from colorama import Fore, Back, Style
from statistics import mean
import sys

def nothing():
    pass

def no_op(args):
    pass

def blockPrint():
    sys.stdout = nothing()

def enablePrint():
    sys.stdout = sys.__stdout__

def write_to_file(filename=None, words=None, mode='w', error=False):
    if error:
        filename = 'error_output'
        mode = 'a'

    with open(filename, mode) as f:
        f.write(words + '\n')


TEST_OUTPUT = False




def game(team1, team2, amp=4, type_of='None', playoffs=None):
    # enable / disable to have a constant / non-constant amp
    if amp != 4:
        amp = 4
    for ply in team1.players:
        ply.no_power = 0
        ply.is_alive = True
    for ply in team2.players:
        ply.no_power = 0
        ply.is_alive = True
    def lineup(team1_lineup, team2_lineup, lineup_index, team1=team1, team2=team2, tiebreak=False):
        #write_to_file(mode='a', words=f"Lineup start between {team1.name} and {team2.name}")

        #team1_lineup and team2_lineup objects being passed into this function are LISTs OF PLAYERS
        #with 9-lineup teams, 104 is the standard game length

        TESSERACT = 0
        length = 104
        #length *= amp
        length += 1
        for var in team1_lineup:
            var.game_length = length+1
        for var in team2_lineup:
            var.game_length = length+1

        for tick in range(1, length):
            living_team1 = []
            living_team2 = []
            yta_team1 = []
            yta_team2 = []
            for pl in team1_lineup:
                if pl.is_alive:
                    living_team1.append(pl)
                    yta_team1.append(pl)
                elif pl.countdown == 0:
                    pl.respawn()
                    living_team1.append(pl)
                    yta_team1.append(pl)
                else:
                    pl.countdown -= 1

            for pl in team2_lineup:
                if pl.is_alive:
                    living_team2.append(pl)
                    yta_team2.append(pl)
                elif pl.countdown == 0:
                    pl.respawn()
                    living_team2.append(pl)
                    yta_team2.append(pl)
                else:
                    pl.countdown -= 1

            sub_count = 0
            while True:
                if not living_team1 and not living_team2:
                    break
                coin = randint(0, 999)
                if coin%2 == 0:
                    #TEAM1 ATTACKING
                    if yta_team1:
                        attacker = choice(yta_team1)
                        yta_team1.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            if living_team2:
                                defender = choice(living_team2)
                                attacker.attack(defender)
                                if not defender.is_alive:
                                    living_team2.remove(defender)
                                    TESSERACT += abs(3*defender.health)
                            else:
                                attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT += attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    elif yta_team2:
                        #TEAM2 DELAYED ATTACK
                        attacker = choice(yta_team2)
                        yta_team2.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT -= attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    else:
                        break
                elif coin%2 == 1:
                    #TEAM2 ATTACKING
                    if yta_team2:
                        attacker = choice(yta_team2)
                        yta_team2.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            if living_team1:
                                defender = choice(living_team1)
                                attacker.attack(defender)
                                if not defender.is_alive:
                                    living_team1.remove(defender)
                                    TESSERACT -= abs(3*defender.health)
                            else:
                                attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT -= attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    elif yta_team1:
                        #TEAM1 DELAYED ATTACK
                        attacker = choice(yta_team1)
                        yta_team1.remove(attacker)
                        if tick % attacker.atk_spd == 0 or attacker.delayed_atk != 0:
                            attacker.delayed_atk += 1
                        if attacker.no_power == 0:
                            TESSERACT += attacker.tesseract()
                        else:
                            attacker.no_power -= 1
                    else:
                        break
                sub_count += 1
        for player in team2.players:
            player.games_played['This-Season'] += 1
        for player in team1.players:
            player.games_played['This-Season'] += 1
        if TESSERACT > 0:
            team1.wins += 1
            team1.margin += abs(round(TESSERACT,2))
            team1.lineup_wins[lineup_index] += 1
            team2.losses += 1
            team2.margin -= abs(round(TESSERACT,2))
            team2.lineup_losses[lineup_index] += 1
            return team1
        else:
            team1.losses += 1
            team1.margin -= abs(round(TESSERACT,2))
            team1.lineup_losses[lineup_index] += 1
            team2.wins += 1
            team2.margin += abs(round(TESSERACT,2))
            team2.lineup_wins[lineup_index] += 1
            return team2
        #end of lineup()

    # if this crashes the code: last functional version 2/7/2024, 11:35 PM

    #todo instead of having this function run a single true_game() based on the coin flip,
    # it will run a game with each lineup. in the playoffs, it will end when one team reaches 8 wins,
    # but in the regular season, it will end only after all 15 lineups have been played
    # I will make playoffs = False in the function parameters, and run playoff = True through the best_of() function
    # through the double_elim() functions
    # true_game() will be renamed to lineup() and continue to return only the winner value
    # but, it will also edit two lists with each game: team.lineup_wins and team.lineup_losses

    lineup_count = 0
    team1_lineups_won = 0
    team2_lineups_won = 0

    for tp1 in team1.players:
        tp1.games_played['Matches'] += 1
    for tp2 in team2.players:
        tp2.games_played['Matches'] += 1

    if not playoffs:
        while lineup_count < (len(team1.lineups)-1):
            #with the current 9-lineup function, the 9th lineup is the first lineup repeated,
            #so it only should apply in the playoffs for a tiebreaker
            #lineup function below
            winner = lineup(team1.lineups[lineup_count],team2.lineups[lineup_count], lineup_index=lineup_count, team1=team1, team2=team2)
            if winner == team1:
                team1_lineups_won += 1
            elif winner == team2:
                team2_lineups_won += 1
            lineup_count += 1
        if team1_lineups_won > team2_lineups_won:
            team1.match_wins += 1
            team2.match_losses += 1
            return team1
        elif team2_lineups_won > team1_lineups_won:
            team2.match_wins += 1
            team1.match_losses += 1
            return team2
        else:
            team1.match_draws += 1
            team2.match_draws += 1
            return choice([team1, team2])

    elif playoffs:
        playoff_dict = playoffs
        playoffs = playoff_dict
        #playoffs equals a dictionary which looks like
        # playoff_objects = {"Team 1 Series Lineups Won" : team1_alt_lineup_wins, "Team 1 Series Lineups Lost" : team1_alt_lineup_losses,
        #                        "Team 2 Series Lineups Won" : team2_alt_lineup_wins, "Team 2 Series Lineups Lost" : team2_alt_lineup_losses,
        #                        "Average Score Dictionary" : avg_match_score}
        playoff_dict['Team 1 Tiebreaker Wins'] = [0,0,0]
        playoff_dict['Team 2 Tiebreaker Wins'] = [0,0,0]

        while team1_lineups_won < 5 and team2_lineups_won < 5:
            if team1_lineups_won == 4 and team2_lineups_won == 4:
                team1_tb = 0
                team2_tb = 0
                tb_index = 0

                team1_tb_wins = [0,0,0]
                team2_tb_wins = [0,0,0]

                while team1_tb < 2 and team2_tb < 2:
                    temp_winner = lineup(team1.lineups[8], team2.lineups[8], lineup_index=lineup_count,
                                    team1=team1, team2=team2)
                    if team1 == temp_winner:
                        team1_tb += 1
                        team1_tb_wins[tb_index] += 1
                    elif team2 == temp_winner:
                        team2_tb += 1
                        team2_tb_wins[tb_index] += 1
                    tb_index += 1

                winner = team1 if team1_tb == 2 else team2
                for num in [0,1,2]:
                    playoffs['Team 1 Tiebreaker Wins'][num] += team1_tb_wins[num]
                    playoffs['Team 2 Tiebreaker Wins'][num] += team2_tb_wins[num]

            else:
                winner = lineup(team1.lineups[lineup_count], team2.lineups[lineup_count], lineup_index=lineup_count,
                                team1=team1, team2=team2)
            if winner == team1:
                playoff_dict["Team 1 Series Lineups Won"][lineup_count] += 1
                playoff_dict["Team 2 Series Lineups Lost"][lineup_count] += 1

                team1_lineups_won += 1
            elif winner == team2:
                playoff_dict["Team 2 Series Lineups Won"][lineup_count] += 1
                playoff_dict["Team 1 Series Lineups Lost"][lineup_count] += 1

                team2_lineups_won += 1

            lineup_count += 1

        playoff_dict["Game Count"] += 1
        playoff_dict["Total Score Dictionary"]["Team 1 Total Lineup Wins"] += team1_lineups_won
        playoff_dict["Total Score Dictionary"]["Team 2 Total Lineup Wins"] += team2_lineups_won

        if team1_lineups_won > team2_lineups_won:
            return team1
        elif team2_lineups_won > team1_lineups_won:
            return team2

def best_of(team1,team2,thresh,amp=4,both_return=False,win_by=1,test_output=False,is_uni=False, upset_list= None, upset_count=None, context=None):

    t_dec_index = 0
    decrease_count = 0

    win_by_immutable = win_by
    trigger = round(mean([-(win_by_immutable * 2), 100]))
    if trigger <= 10:
        trigger = 21
    elif trigger < 20:
        trigger = 18

    end_decrease = win_by_immutable / 3

    blockPrint()
    team1_wins = 0
    team2_wins = 0
    game_count = 0

    # DONE because any best_of series will be a playoff game, I need to inform each iteration of game() of this
    # so that it only runs each game to 8 won lineups
    # once I make this change in game(), I need to come back to this and run playoff=True through each iteration of
    # game()
    team1_alt_lineup_wins = [0] * 9
    team1_alt_lineup_losses = [0] * 9
    team2_alt_lineup_wins = [0] * 9
    team2_alt_lineup_losses = [0] * 9
    total_match_score = {"Team 1 Total Lineup Wins" : 0, "Team 2 Total Lineup Wins" : 0}

    playoff_objects = {"Team 1 Series Lineups Won" : team1_alt_lineup_wins, "Team 1 Series Lineups Lost" : team1_alt_lineup_losses,
                       "Team 2 Series Lineups Won" : team2_alt_lineup_wins, "Team 2 Series Lineups Lost" : team2_alt_lineup_losses,
                       "Total Score Dictionary" : total_match_score, "Game Count" : 0, "Team 1 Tiebreaker Wins" : [0,0,0],
                       "Team 2 Tiebreaker Wins" : [0,0,0]}

    def print_lineup_score(team1_lineup_wins, team1_lineup_losses, team2_lineup_wins, team2_lineup_losses,
                           team1_total_wins, team2_total_wins, team1_tb_wins, team2_tb_wins):
        #team1 is the WINNING TEAM, and team2 is the LOSING TEAM, regardless of what they are in the game
        length = 0
        total_games_played = team1_total_wins + team2_total_wins
        output_str = " ["
        if len(team1_lineup_wins) == len(team2_lineup_wins):
            length = len(team1_lineup_wins)

        for i in range(length):
            if team2_lineup_wins[i] > team1_lineup_wins[i]:
                output_str += "*"
            output_str += f"{i}N({team1_lineup_wins[i]}-{team2_lineup_wins[i]})"
            if team2_lineup_wins[i] > team1_lineup_wins[i]:
                output_str += "*"
            if i < length-1:
                output_str += ", "
            #the below code is part of an abandoned project to make each tiebreaker a 2 of 3 instead of one game
            #else:
            #    output_str += " |"
            #    for num in [0,1,2]:
            #        output_str += f"{team1_tb_wins[num]}-{team2_tb_wins[num]}"
            #        if num != 2:
            #            output_str += ", "
            #    output_str += "|"

        non_sweeps = team1_lineup_wins[5] + team2_lineup_wins[5]
        sweeps = total_games_played - non_sweeps

        tiebreak_games_played = team1_lineup_wins[8] + team2_lineup_wins[8]
        output_str += f"] TOTAL: {sum(team1_lineup_wins)}-{sum(team2_lineup_wins)}"
        tiebreak_str = f" ({tiebreak_games_played} of {total_games_played}" \
                       f" [{(tiebreak_games_played / total_games_played)*100:.2f}%] reached a tiebreak, and " \
                       f"{sweeps} of {total_games_played} [{(sweeps / total_games_played)*100:.2f}%]" \
                       f" were 5-0 sweeps.)"
        #



        return output_str, tiebreak_str

    while True:
        #playoffs= is supposed to take in a dictionary with several objects
        # list of team1 and team2 lineup wins (list 15 elements long, all initialized to 0)
        # avg_score, initialized to 0

        winner = game(team1, team2, amp, playoffs=playoff_objects)
        team1_wins += 1 if winner == team1 else 0
        team2_wins += 1 if winner == team2 else 0
        game_count += 1
        if team1_wins == thresh or team2_wins == thresh:
            break

    while abs(team1_wins - team2_wins) < win_by:
        winner = game(team1, team2, amp, playoffs=playoff_objects)
        team1_wins += 1 if winner == team1 else 0
        team2_wins += 1 if winner == team2 else 0
        game_count += 1
        if game_count > thresh*5 and decrease_count < end_decrease:
            t_dec_index += 1
        if t_dec_index == trigger and decrease_count < end_decrease:
            win_by -= 1
            decrease_count += 1
            t_dec_index = 0
    if decrease_count != 0:
        write_to_file(error=True, words = f"\nIn a series between {team1.name} and {team2.name}, the margin was decreased from {win_by_immutable} to {win_by}."
                                          f"\nThe margin was decreased every {trigger} games after reaching {thresh*5} games.\n")
        if decrease_count == end_decrease:
            write_to_file(error=True, words=f"The limit of {end_decrease} was hit in this series, meaning that the margin of victory stuck at {win_by}")

    for player in team2.players:
        player.games_played['Playoffs'] += 1
    for player in team1.players:
        player.games_played['Playoffs'] += 1

    #reminder playoff_objects = {"Team 1 Series Lineups Won" : team1_alt_lineup_wins, "Team 1 Series Lineups Lost" : team1_alt_lineup_losses,
    #                   "Team 2 Series Lineups Won" : team2_alt_lineup_wins, "Team 2 Series Lineups Lost" : team2_alt_lineup_losses,
    #                   "Average Score Dictionary" : avg_match_score}

    t1_avg_series_wins = playoff_objects["Total Score Dictionary"]["Team 1 Total Lineup Wins"] / game_count
    t2_avg_series_wins = playoff_objects["Total Score Dictionary"]["Team 2 Total Lineup Wins"] / game_count

    if team1_wins > team2_wins:
        lineup_statement, tiebreak_statement = print_lineup_score(team1_lineup_wins=playoff_objects['Team 1 Series Lineups Won'],
                                              team1_lineup_losses=playoff_objects['Team 1 Series Lineups Lost'],
                                              team2_lineup_wins=playoff_objects['Team 2 Series Lineups Won'],
                                              team2_lineup_losses=playoff_objects['Team 2 Series Lineups Lost'],
                                              team1_total_wins=team1_wins, team2_total_wins=team2_wins,
                                              team1_tb_wins=playoff_objects['Team 1 Tiebreaker Wins'],
                                              team2_tb_wins=playoff_objects['Team 2 Tiebreaker Wins'])
        enablePrint()
        if team1.seed != -1:
            print(Back.RED + Fore.BLACK +
                f"{team1.name}({team1.seed}) defeat {team2.name}({team2.seed}) by a score of {team1_wins}-{team2_wins}." + Fore.BLUE + Back.RESET + lineup_statement + Fore.RESET + tiebreak_statement)
            if team1.seed > team2.seed:
                upset_count += 1
                temp_context = f"{team1.seed}({team1.name}) def. {team2.seed}({team2.name}) by a score of {team1_wins}-{team2_wins} ({context})"
                seed_diff = team1.seed - team2.seed
                upset_obj = tuple([temp_context, seed_diff])
                upset_list.append(upset_obj)
        else:
            print(Back.RED + Fore.BLACK +
                f"{team1.name} defeat {team2.name} by a score of {team1_wins}-{team2_wins}." + Fore.BLUE + Back.RESET + lineup_statement + Fore.RESET + tiebreak_statement)
        if test_output:
            print(series_test(team1_wins, team2_wins))

        if is_uni:
            team1.accolades['Uni-Playoff-Wins'] += 1
        if not both_return:
            return team1
        else:
            return team1, team2
    else:
        lineup_statement, tiebreak_statement = print_lineup_score(team1_lineup_wins=playoff_objects['Team 2 Series Lineups Won'],
                                              team1_lineup_losses=playoff_objects['Team 2 Series Lineups Lost'],
                                              team2_lineup_wins=playoff_objects['Team 1 Series Lineups Won'],
                                              team2_lineup_losses=playoff_objects['Team 1 Series Lineups Lost'],
                                              team1_total_wins=team2_wins, team2_total_wins=team1_wins,
                                              team1_tb_wins=playoff_objects['Team 2 Tiebreaker Wins'],
                                              team2_tb_wins=playoff_objects['Team 1 Tiebreaker Wins'])

        enablePrint()
        if team2.seed != -1:
            print(Back.RED + Fore.BLACK +
                f"{team2.name}({team2.seed}) defeat {team1.name}({team1.seed}) by a score of {team2_wins}-{team1_wins}." + Fore.BLUE + Back.RESET + lineup_statement + Fore.RESET + tiebreak_statement)
            if team2.seed > team1.seed:
                upset_count += 1
                temp_context = f"{team2.seed}({team2.name}) def. {team1.seed}({team1.name}) by a score of {team2_wins}-{team1_wins} ({context})"
                seed_diff = team2.seed - team1.seed
                upset_obj = tuple([temp_context, seed_diff])
                upset_list.append(upset_obj)
        else:
            print(Back.RED + Fore.BLACK +
                f"{team2.name} defeat {team1.name} by a score of {team2_wins}-{team1_wins}." + Fore.BLUE + Back.RESET + lineup_statement + Fore.RESET + tiebreak_statement)
        if test_output:
            print(series_test(team2_wins, team1_wins))
        if is_uni:
            team2.accolades['Uni-Playoff-Wins'] += 1
        if not both_return:
            return team2
        else:
            return team2, team1
