from pickle import load

def season_wipe(teams):
    for team in teams:
        team.wins = 0
        team.losses = 0
        team.match_wins = 0
        team.match_losses = 0
        team.match_draws = 0
        team.trophies = 0
        team.seed = -1
        team.margin = 0

        for i in range(len(team.lineup_losses)):
            team.lineup_wins[i] = 0
            team.lineup_losses[i] = 0

        for player in team.players:
            player.kills = 0
            player.crit_kills = 0
            player.deaths = 0
            player.crit_data = {'Hit' : 0.0, 'Miss' : 0.0, 'Ratio' : 0.0, 'Parry' : 0.0, 'P_Miss' : 0, "P_Ratio" : 0.0, "Mitigated" : 0.0}
            player.kill_streak = {'Current' : 0, 'Peak' : 0}
            player.damage_data = {'Tesseract': 0.0, 'Total-Attacks': 0, 'Total-Damage': 0.0, 'Total-Delayed-Damage': 0.0,
                                'Total-Delayed-X': 0.0, 'Delayed-Count': 0, 'Avg-Delayed-X': 0.0,
                                'Avg-Delayed-Damage': 0.0, 'Overkill': 0.0, 'Overkill-Count': 0, 'Revived' : 0, 'Healed' : 0, 'Reflected' : 0.0, 'Reflect-Kills' : 0}
            total_games = player.games_played['All'] + player.games_played['This-Season']
            player.games_played = {'This-Season' : 0, 'All': total_games, 'Playoffs': 0, 'Matches' : 0}
            for key in player.damage_data.keys():
                player.damage_data[key] = 0

    return teams

def load_pkl() -> object:
    with open("database.pkl", 'rb') as f:
        saved_TEAMS = load(f)
        if len(saved_TEAMS) == 10:
            return saved_TEAMS
        elif len(saved_TEAMS) == 9:
            return saved_TEAMS
def load_season():
    with open("champ_data.pkl", 'rb') as f:
        season_count = load(f)
        return season_count
