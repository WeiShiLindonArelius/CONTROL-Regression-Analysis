from Games import game, no_op, blockPrint, enablePrint, best_of
from random import choice
from colorama import Fore
from load_pickle import season_wipe

# todo edit print_standings to print normal record AND lineup record
# which can be accessed from team.lineup_wins and team.lineup_losses
def print_standings(TEAMS,universal=False):
    enablePrint()
    print(Fore.GREEN + f"ROBIN STANDINGS" + Fore.RESET)

    idx = 0
    TEAMS.sort(key=lambda x: (x.wins, x.points, x.margin), reverse=True)
    for team in TEAMS:
        temp_lineup_record = f"\t[0N({team.lineup_wins[0]}-{team.lineup_losses[0]}), " \
                             f"1N({team.lineup_wins[1]}-{team.lineup_losses[1]}), " \
                             f"2N({team.lineup_wins[2]}-{team.lineup_losses[2]}), " \
                             f"3N({team.lineup_wins[3]}-{team.lineup_losses[3]}), " \
                             f"4N({team.lineup_wins[4]}-{team.lineup_losses[4]}), " \
                             f"5N({team.lineup_wins[5]}-{team.lineup_losses[5]}), " \
                             f"6N({team.lineup_wins[6]}-{team.lineup_losses[6]}), " \
                             f"7N({team.lineup_wins[7]}-{team.lineup_losses[7]})]"

        idx += 1
        team.seed = idx
        if team.margin <= 0:
            sign = ''
        else:
            sign = '+'
        print(f"{idx}. {team.name}: {team.wins}-{team.losses} ({team.match_wins}-{team.match_losses}-{team.match_draws} match record)"
              + Fore.GREEN + f"{temp_lineup_record}" + Fore.RESET + f" [[{sign}{round(team.margin,2)}]]")

def round_robin(TEAMS,r,qualify_range,amp=4,alt_qualify_range = None, is_test=False):
    if is_test:
        for team in TEAMS:
            team.wins = team.losses = 0
    SIZE = len(TEAMS)
    for k in range(r):
        for i in range(SIZE):
            for j in range(i + 1, SIZE):
                team1 = TEAMS[i]
                team2 = TEAMS[j]
                game(team1, team2,amp)
        if k == r-1:
            for team in TEAMS:
                team.points = (3*team.match_wins) + team.match_draws
            TEAMS.sort(key=lambda x: (x.wins, x.points, x.margin), reverse=True)
            print_standings(TEAMS, True)
    if qualify_range == 1:
        return TEAMS[0]
    else:
        bebop = []
        bebop2 = []
        for q in range(qualify_range):
            bubba = TEAMS[q]
            bebop.append(bubba)
        if alt_qualify_range:
            for q in range(qualify_range, qualify_range+alt_qualify_range):
                bubba2 = TEAMS[q]
                bebop2.append(bubba2)
            return bebop, bebop2
        else:
            return bebop

def chain(teams):
    size = len(teams)
    winner = best_of(teams[size], teams[size-1], 100, win_by=10)
    for i in range(size):
        winner = best_of(winner, teams[size-i], 100+i, win_by=10)
    return winner