# fbref_config.py

# URLs for different football league stats pages on FBref
FBREF_URLS = {
    "Premier_League": "https://fbref.com/en/comps/9/Premier-League-Stats",
    "Serie_A": "https://fbref.com/en/comps/11/Serie-A-Stats",
    "La_Liga": "https://fbref.com/en/comps/12/La-Liga-Stats",
    "Ligue_1": "https://fbref.com/en/comps/13/Ligue-1-Stats",
    "Bundesliga": "https://fbref.com/en/comps/20/Bundesliga-Stats"
}

# Player stats URLs for each league
FBREF_PLAYERS_STATS_URLS = {
    "Premier_League": [
        "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
        "https://fbref.com/en/comps/9/keepers/Premier-League-Stats",
        "https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats",
        "https://fbref.com/en/comps/9/shooting/Premier-League-Stats",
        "https://fbref.com/en/comps/9/passing/Premier-League-Stats",
        "https://fbref.com/en/comps/9/passing_types/Premier-League-Stats",
        "https://fbref.com/en/comps/9/gca/Premier-League-Stats",
        "https://fbref.com/en/comps/9/defense/Premier-League-Stats",
        "https://fbref.com/en/comps/9/possession/Premier-League-Stats",
        "https://fbref.com/en/comps/9/playingtime/Premier-League-Stats",
        "https://fbref.com/en/comps/9/misc/Premier-League-Stats"
    ],
    "La_Liga": [
        "https://fbref.com/en/comps/12/stats/La-Liga-Stats",
        "https://fbref.com/en/comps/12/keepers/La-Liga-Stats",
        "https://fbref.com/en/comps/12/keepersadv/La-Liga-Stats",
        "https://fbref.com/en/comps/12/shooting/La-Liga-Stats",
        "https://fbref.com/en/comps/12/passing/La-Liga-Stats",
        "https://fbref.com/en/comps/12/passing_types/La-Liga-Stats",
        "https://fbref.com/en/comps/12/gca/La-Liga-Stats",
        "https://fbref.com/en/comps/12/defense/La-Liga-Stats",
        "https://fbref.com/en/comps/12/possession/La-Liga-Stats",
        "https://fbref.com/en/comps/12/playingtime/La-Liga-Stats",
        "https://fbref.com/en/comps/12/misc/La-Liga-Stats"
    ],
    "Serie_A": [
        "https://fbref.com/en/comps/11/stats/Serie-A-Stats",
        "https://fbref.com/en/comps/11/keepers/Serie-A-Stats",
        "https://fbref.com/en/comps/11/keepersadv/Serie-A-Stats",
        "https://fbref.com/en/comps/11/shooting/Serie-A-Stats",
        "https://fbref.com/en/comps/11/passing/Serie-A-Stats",
        "https://fbref.com/en/comps/11/passing_types/Serie-A-Stats",
        "https://fbref.com/en/comps/11/gca/Serie-A-Stats",
        "https://fbref.com/en/comps/11/defense/Serie-A-Stats",
        "https://fbref.com/en/comps/11/possession/Serie-A-Stats",
        "https://fbref.com/en/comps/11/playingtime/Serie-A-Stats",
        "https://fbref.com/en/comps/11/misc/Serie-A-Stats"
    ],
    "Bundesliga": [
        "https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/keepers/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/keepersadv/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/shooting/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/passing/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/passing_types/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/gca/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/defense/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/possession/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/playingtime/Bundesliga-Stats",
        "https://fbref.com/en/comps/20/misc/Bundesliga-Stats"
    ],
    "Ligue_1": [
        "https://fbref.com/en/comps/13/stats/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/keepers/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/keepersadv/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/shooting/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/passing/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/passing_types/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/gca/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/defense/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/possession/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/playingtime/Ligue-1-Stats",
        "https://fbref.com/en/comps/13/misc/Ligue-1-Stats"
    ]
}


# File paths for leagues
LEAGUE_PATHS = {
    "Bundesliga": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Bundesliga\Bundesliga_Squad_Standard_Stats_cleaned.csv",
    "La_Liga": r"C:\Users\asus\Desktop\Football_project\cleaned_data\La_Liga\La_Liga_Squad_Standard_Stats_cleaned.csv",
    "Ligue_1": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Ligue_1\Ligue_1_Squad_Standard_Stats_cleaned.csv",
    "Premier_League": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Premier_League\Premier_League_Squad_Standard_Stats_cleaned.csv",
    "Serie_A": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Serie_A\Serie_A_Squad_Standard_Stats_cleaned.csv"
}

# File paths for players
PLAYERS_PATHS = {
    "Bundesliga": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Bundesliga\Standard_cleaned.csv",
    "La_Liga": r"C:\Users\asus\Desktop\Football_project\cleaned_data\La_Liga\Standard_cleaned.csv",
    "Ligue_1": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Ligue_1\Standard_cleaned.csv",
    "Premier_League": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Premier_League\Standard_cleaned.csv",
    "Serie_A": r"C:\Users\asus\Desktop\Football_project\cleaned_data\Serie_A\Standard_cleaned.csv"
}

# Save folder for final tables
SAVE_FOLDER = r"C:\Users\asus\Desktop\Football_project\first_tables"


