from stat_functions import series_test
import pandas as pd
from sklearn.linear_model import LinearRegression
from Teams import Team
from contests import round_robin
from multiprocessing import Process, Lock



def test_robin():
    TEAMS = []
    for i in range(50):
        temp = Team('Universal')
        TEAMS.append(temp)

    atk_dmg_list = {}
    atk_spd_list = {}
    crit_pct_list = {}
    crit_x_list = {}
    health_list = {}
    power_list = {}
    spawn_list = {}
    win_list = []

    avg_atk_dmg_list = []
    avg_atk_spd_list = []
    avg_crit_pct_list = []
    avg_crit_x_list = []
    avg_health_list = []
    avg_power_list = []
    avg_spawn_list = []


    round_robin(TEAMS,36,1,2)
    for team in TEAMS:
        sum_atk_dmg = 0
        sum_atk_spd = 0
        sum_crit_pct = 0
        sum_crit_x = 0
        sum_health = 0
        sum_power = 0
        sum_spawn = 0

        atk_dmg_list[team.name] = []
        atk_spd_list[team.name] = []
        crit_pct_list[team.name] = []
        crit_x_list[team.name] = []
        health_list[team.name] = []
        power_list[team.name] = []
        spawn_list[team.name] = []


        win_list.append(team.wins)
        for player in team.players:
            atk_dmg_list[team.name].append(player.atk_dmg)
            sum_atk_dmg += player.atk_dmg
            atk_spd_list[team.name].append(player.atk_spd)
            sum_atk_spd += player.atk_spd
            crit_pct_list[team.name].append(player.crit_pct)
            sum_crit_pct += 100*player.crit_pct
            crit_x_list[team.name].append(player.crit_x)
            sum_crit_x += player.crit_x
            health_list[team.name].append(player.max_health)
            sum_health += player.max_health
            power_list[team.name].append(player.power)
            sum_power += player.power
            spawn_list[team.name].append(player.spawn_time)
            sum_spawn += player.spawn_time
        avg_atk_dmg_list.append(sum_atk_dmg / len(team.players))
        avg_atk_spd_list.append(sum_atk_spd / len(team.players))
        avg_crit_pct_list.append(sum_crit_pct / len(team.players))
        avg_crit_x_list.append(sum_crit_x / len(team.players))
        avg_health_list.append(sum_health / len(team.players))
        avg_power_list.append(sum_power / len(team.players))
        avg_spawn_list.append(sum_spawn / len(team.players))


    data_dict = { 'ATK_DMG' : avg_atk_dmg_list, 'ATK_SPD' : avg_atk_spd_list, 'CRIT_PCT' : avg_crit_pct_list, 'CRIT_X' : avg_crit_x_list, 'HEALTH' : avg_health_list, 'POWER' : avg_power_list, 'SPAWN' : avg_spawn_list, 'Y' : win_list}
    df = pd.DataFrame.from_dict(data_dict, orient='columns')
    x = df.iloc[:, :-1].values
    print(x)
    y = df.iloc[:, -1].values
    print(y)
    regressor = LinearRegression()
    regressor.fit(x, y)
    coefficients = regressor.coef_
    intercept = regressor.intercept_
    line_of_best_fit = f"PREDICTED_WINS = {intercept:.3f} , {coefficients[0]:.6f}(ATK_DMG), {coefficients[1]:.6f}(ATK_SPD), {coefficients[2]:.6f}(CRIT_PCT), {coefficients[3]:.6f}(CRIT_X), {coefficients[4]:.6f}(HEALTH), {coefficients[5]:.6f}(POWER), {coefficients[6]:.6f}(SPAWN_TIME)"
    print(line_of_best_fit)

test_robin()
