from scipy.stats import binomtest
from colorama import Fore
import numpy as np
from Players import PlayerSeason, grade_seasons


def write_to_file(filename=None, words=None, mode='w', error=False):
    if error:
        filename = 'error_output'
        mode = 'a'

    with open(filename, mode) as f:
        f.write(words + '\n')

def check_equal_season(season1,season2):
    if season1.kills == season2.kills and season1.damage == season2.damage and season1.mitigated == season2.mitigated:
        return True
    else:
        return False

def remove_duplicate_seasons(seasons):
    seen_seasons = []
    unique_seasons = []

    for season in seasons:
        if not any(check_equal_season(season, seen_season) for seen_season in seen_seasons):
            unique_seasons.append(season)
            seen_seasons.append(season)

    return unique_seasons

def season_stats(league, season_count, season_stats_list, alt_stats_list = None,  do_print=False):
    #make season_stats_list into a dict with int keys for season number and values of lists of PlayerSeasons
    region = ""
    season_stats_list[season_count] = []
    total_pl_kills = 0
    total_pl_deaths = 0

    total_szn_kills = 0
    total_szn_deaths = 0

    for team in league:
        region = team.region
        for player in team.players:
            if True:
                stats = PlayerSeason(player, season_count)
                total_szn_kills += (stats.kills * stats.game_count)
                total_szn_deaths += (stats.deaths * stats.game_count)

                total_pl_kills += player.kills
                total_pl_deaths += player.deaths
                season_stats_list[season_count].append(stats)
                if alt_stats_list:
                    alt_stats_list.append(stats)

    return season_stats_list[season_count]


def region_mvp(season_stats_list, season_count, region):
    full_season_list = season_stats_list[season_count]


    with open('region_mvp.txt', 'a') as p:
        p.write(f"{region} S{season_count} MVP\n")
        grade_seasons(full_season_list, print_averages=False, context=f"{region} Regular Season\n", region=region)
        full_season_list.sort(key=lambda s : s.season_grade_data, reverse=True)
    full_season_list[0].print_player_season('region_mvp.txt')

def best_of_stats(season_stats_list, season_count, alt_stats_list=None, avg_stats_df = None):

    full_season_list = []
    for val in season_stats_list.values():
        for season in val:
            full_season_list.append(season)

    full_season_list = remove_duplicate_seasons(full_season_list)

    BIG_RANGE = 15 if len(full_season_list) >= 15 else 0
    SMALL_RANGE = 3 if len(full_season_list) > 3 else 0


    with open('best_stats', 'a') as p:
        p.write("ALL TIME BEST SEASONS (251+ games to qualify for stats): \n")
        grade_seasons(full_season_list, context=f"FULL SEASON no. {season_count} LIST WITH {len(full_season_list)} values!\n", avg_stats_df=avg_stats_df, region='All')

        full_season_list.sort(key=lambda s : s.season_grade_data, reverse=True)
        for szn in full_season_list:
            if szn.game_count < 251:
                full_season_list.remove(szn)

    for i in range(BIG_RANGE):
        full_season_list[i].print_player_season('best_stats')




    full_season_list.sort(key=lambda s : s.kills, reverse=True)
    with open('best_stats', 'a') as p:
        p.write('MOST KILLS\n\n')
    for i in range(SMALL_RANGE):
        full_season_list[i].print_kills_deaths()

    full_season_list.sort(key=lambda s: s.streak, reverse=True)
    with open('best_stats', 'a') as p:
        p.write("//////////////\n\nLONGEST KILL STREAK\n\n")
    for i in range(SMALL_RANGE):
        full_season_list[i].print_streak()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nLEAST DEATHS\n\n')
    full_season_list.sort(key=lambda s: s.deaths)
    for i in range(SMALL_RANGE):
        full_season_list[i].print_kills_deaths()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nMOST DAMAGE DEALT\n\n')
    full_season_list.sort(key=lambda s: s.damage, reverse=True)
    for i in range(SMALL_RANGE):
        full_season_list[i].print_damage()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nMOST DAMAGE MITIGATED\n\n')
    full_season_list.sort(key=lambda s: s.mitigated, reverse=True)
    for i in range(SMALL_RANGE):
        full_season_list[i].print_mitigated()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nLARGEST TOTAL EFFECT\n\n')
    full_season_list.sort(key=lambda s: s.effect, reverse=True)
    for i in range(SMALL_RANGE):
        full_season_list[i].print_effect()

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nLARGEST OVERKILL EFFECT\n\n')
    full_season_list.sort(key=lambda s: s.overkill, reverse=True)
    for i in range(SMALL_RANGE):
        full_season_list[i].print_effect()



def series_test(wins, losses):
    result = binomtest(wins, wins+losses, 0.50)
    p_val = result.pvalue
    np.set_printoptions(precision=4, suppress=True)
    return Fore.CYAN + f"There is a {round((p_val*100),8)}% chance the result was due to chance alone." + Fore.RESET