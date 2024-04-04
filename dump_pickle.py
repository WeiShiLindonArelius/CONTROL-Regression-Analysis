from pickle import dump

def dump_pkl(TEAMS):
    with open("database.pkl", 'wb') as f:
        dump(TEAMS,f)

def dump_champ(champ_team):
    with open('champ_data.pkl', 'wb') as f:
        dump(champ_team,f)