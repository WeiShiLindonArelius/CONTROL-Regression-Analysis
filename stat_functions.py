import sqlite3

from scipy.stats import binomtest
from colorama import Fore
import numpy as np
from Players import PlayerSeason, grade_seasons, NO_SQL
import pandas as pd

def QUERY(sql, connect=sqlite3.connect('ControlDataBase.db'), params=None, is_select=False):
    if NO_SQL:
        return 0
    elif is_select:
        if params:
            return pd.read_sql_query(sql, connect, params=params)
        else:
            return pd.read_sql_query(sql, connect)
    else:
        cur = connect.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        connect.commit()
        return cur.lastrowid

def clear_all_databases():
    connect = sqlite3.connect('ControlDataBase.db')
    query = "DROP TABLE IF EXISTS Game;"
    QUERY(query, connect, is_select=False)

    query = "DROP TABLE IF EXISTS Match;"
    QUERY(query, connect, is_select=False)

    query = "DROP TABLE IF EXISTS Series;"
    QUERY(query, connect, is_select=False)

    query = "DROP TABLE IF EXISTS Team;"
    QUERY(query, connect, is_select=False)

    query = "DROP TABLE IF EXISTS Player;"
    QUERY(query, connect, is_select=False)

    query = "DROP TABLE IF EXISTS TotalSeason;"
    QUERY(query, connect, is_select=False)

    query = "DROP TABLE IF EXISTS TeamSeason"
    QUERY(query, connect, is_select=False)
def initiate_databases():
    connect = sqlite3.connect("ControlDataBase.db")
    query = """ CREATE TABLE IF NOT EXISTS Team (
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT,
                region_of_origin TEXT,
                season_of_origin INTEGER)
    """
    QUERY(query, connect, is_select=False)
    query = """ CREATE TABLE IF NOT EXISTS Player (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                amp REAL,
                tier TEXT,
                trait TEXT,
                player_name TEXT,
                season_of_origin INTEGER)
    """
    QUERY(query, connect, is_select=False)
    query = """ CREATE TABLE IF NOT EXISTS Game (
                    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    winning_team_id INTEGER REFERENCES Team(team_id),
                    losing_team_id INTEGER REFERENCES Team(team_id),
                    margin_of_victory REAL,
                    lineup_count INTEGER,
                    playoffs INTEGER)        
        """
    QUERY(query, connect, is_select=False)
    query = """ CREATE TABLE IF NOT EXISTS Match (
                        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        winning_team_id INTEGER REFERENCES Team(team_id),
                        losing_team_id INTEGER REFERENCES Team(team_id),
                        match_score TEXT,
                        _0N_winner_id INTEGER REFERENCES Team(team_id),
                        _1N_winner_id INTEGER REFERENCES Team(team_id),
                        _2N_winner_id INTEGER REFERENCES Team(team_id),
                        _3N_winner_id INTEGER REFERENCES Team(team_id),
                        _4N_winner_id INTEGER REFERENCES Team(team_id),
                        _5N_winner_id INTEGER REFERENCES Team(team_id),
                        _6N_winner_id INTEGER REFERENCES Team(team_id),
                        _7N_winner_id INTEGER REFERENCES Team(team_id),
                        _8N_winner_id INTEGER REFERENCES Team(team_id),
                        playoffs TEXT)        
            """
    QUERY(query, connect, is_select=False)
    query = """ CREATE TABLE IF NOT EXISTS Series (
                                series_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                winning_team_id INTEGER REFERENCES Team(team_id),
                                losing_team_id INTEGER REFERENCES Team(team_id),
                                winning_seed BLOB,
                                losing_seed BLOB,
                                seed_diff BLOB,
                                winner_name TEXT,
                                loser_name TEXT,
                                series_score TEXT,
                                _0N_score TEXT,
                                _1N_score TEXT,
                                _2N_score TEXT,
                                _3N_score TEXT,
                                _4N_score TEXT,
                                _5N_score TEXT,
                                _6N_score TEXT,
                                _7N_score TEXT,
                                _8N_score TEXT,
                                series_game_score TEXT,
                                context TEXT)        
                    """
    QUERY(query, connect, is_select=False)
    query = """ CREATE TABLE IF NOT EXISTS TotalSeason (
                                season_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                uni_champ_id INTEGER REFERENCES Team(team_id),
                                biggest_upset TEXT,
                                darkwing_champ_id INTEGER REFERENCES Team(team_id),
                                shining_core_champ_id INTEGER REFERENCES Team(team_id),
                                diamond_sea_champ_id INTEGER REFERENCES Team(team_id),
                                web_of_nations_champ_id INTEGER REFERENCES Team(team_id),
                                ice_wall_champ_id INTEGER REFERENCES Team(team_id),
                                candyland_champ_id INTEGER REFERENCES Team(team_id),
                                hells_circle_champ_id INTEGER REFERENCES Team(team_id),
                                steel_heart_champ_id INTEGER REFERENCES Team(team_id))        
                    """
    QUERY(query, connect, is_select=False)


    return 0


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

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nBEST HEALERS\n\n')
    full_season_list.sort(key=lambda s: s.healed, reverse=True)
    for i in range(SMALL_RANGE):
        full_season_list[i].print_player_season('best_stats')

    with open('best_stats', 'a') as p:
        p.write('//////////////\n\nBEST REFLECTORS\n\n')
    full_season_list.sort(key=lambda s: s.reflected, reverse=True)
    for i in range(SMALL_RANGE):
        full_season_list[i].print_player_season('best_stats')

def finalize_series_data():
    query = """
        UPDATE Series
        SET winning_seed = 
    CASE
        WHEN instr(winner_name, '(') = 0 OR instr(winner_name, ')') = 0 THEN CAST('n/a' AS BLOB)
        ELSE CAST(
                substr(
                    winner_name, 
                    instr(winner_name, '(') + 1, 
                    instr(winner_name, ')') - instr(winner_name, '(') - 1
                ) AS INTEGER
            )
    END;  """
    QUERY(query)
    query = """
        UPDATE Series
        SET losing_seed = 
    CASE
        WHEN instr(loser_name, '(') = 0 OR instr(loser_name, ')') = 0 THEN CAST('n/a' AS BLOB)
        ELSE CAST(
                substr(
                    loser_name, 
                    instr(loser_name, '(') + 1, 
                    instr(loser_name, ')') - instr(loser_name, '(') - 1
                ) AS INTEGER
            )
    END;  """
    QUERY(query)
    query = """
    UPDATE Series
    SET seed_diff = CASE
        WHEN winning_seed LIKE '%n/a%' OR losing_seed LIKE '%n/a%' THEN CAST('n/a' AS BLOB)
        ELSE (winning_seed - losing_seed)
        END;
    """
    QUERY(query)


def series_test(wins, losses):
    result = binomtest(wins, wins+losses, 0.50)
    p_val = result.pvalue
    np.set_printoptions(precision=4, suppress=True)
    return Fore.CYAN + f"There is a {round((p_val*100),8)}% chance the result was due to chance alone." + Fore.RESET
