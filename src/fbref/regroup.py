import pandas as pd
import os

class RegroupData:
    def __init__(self, save_folder):
        self.save_folder = save_folder
        os.makedirs(save_folder, exist_ok=True)

    def create_league_table(self):
        # Create a DataFrame with League IDs and Names
        league_data = {
            'ID': [1, 2, 3, 4, 5],
            'league_name': ['Bundesliga', 'La_Liga', 'Ligue_1', 'Premier_League', 'Serie_A']
        }
        df_leagues = pd.DataFrame(league_data)

        # Save the DataFrame to a CSV
        league_file_path = os.path.join(self.save_folder, 'leagues.csv')
        df_leagues.to_csv(league_file_path, index=False)
        print(f"Leagues table saved to {league_file_path}")

    def create_team_table(self, league_paths):
        # Initialize an empty DataFrame for all teams
        teams_df = pd.DataFrame()

        # Loop through each league CSV
        for league, path in league_paths.items():
            df = pd.read_csv(path)

            # Extract the 'Squad' column, rename it to 'team_name'
            df_teams = df[['Squad']].copy()
            df_teams.columns = ['team_name']

            # Append teams to the main DataFrame
            teams_df = pd.concat([teams_df, df_teams], ignore_index=True)

        # Remove duplicate teams
        teams_df.drop_duplicates(subset='team_name', inplace=True)

        # Save the result as CSV
        team_file_path = os.path.join(self.save_folder, 'teams.csv')
        teams_df.to_csv(team_file_path, index=False)
        print(f"Teams table saved to {team_file_path}")

    def create_player_table(self, player_paths):
        # Initialize an empty DataFrame for all players
        players_df = pd.DataFrame()

        # Loop through each league's player CSV
        for league, path in player_paths.items():
            df = pd.read_csv(path)

            # Extract relevant columns and rename them
            df_players = df[['Player', 'Nation', 'Pos', 'Age', 'Born']].copy()
            df_players.columns = ['player_name', 'nation', 'position', 'age', 'date_of_birth']

            # Append players to the main DataFrame
            players_df = pd.concat([players_df, df_players], ignore_index=True)

        # Remove duplicate players
        players_df.drop_duplicates(subset='player_name', inplace=True)

        # Save the result as CSV
        player_file_path = os.path.join(self.save_folder, 'players.csv')
        players_df.to_csv(player_file_path, index=False)
        print(f"Players table saved to {player_file_path}")
