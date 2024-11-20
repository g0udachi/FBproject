import os
import pandas as pd
import uuid
from supabase import create_client, Client
from database.db_connection import DatabaseConnection

class DataInserter:
    def __init__(self):
        self.db = DatabaseConnection().get_client()

    def generate_unique_stat_id(self):
        """Generate a unique stat_id using UUID."""
        return uuid.uuid4().int  # Generates a unique integer ID

    def insert_csv_to_table(self, csv_path, table_name, primary_key_field):
        # Read the CSV file using pandas
        df = pd.read_csv(csv_path)

        # Convert the dataframe to a list of dictionaries for inserting into Supabase
        data_to_insert = df.to_dict(orient='records')

        # Assign unique 'stat_id' for tables that use 'stat_id' if missing
        for record in data_to_insert:
            primary_key_value = record.get(primary_key_field)

            # If stat_id is missing or NaN, generate a unique one using UUID
            if primary_key_field == 'stat_id' and (pd.isna(primary_key_value) or primary_key_value is None):
                record['stat_id'] = self.generate_unique_stat_id()

            # Skip records where the primary key is None or NaN
            if primary_key_value is None or pd.isna(primary_key_value):
                print(f"Skipping record with no {primary_key_field} in {table_name}")
                continue

            # Query the database to see if a record with this primary key exists
            existing_record = self.db.table(table_name).select(primary_key_field).eq(primary_key_field, primary_key_value).execute()

            if existing_record.data:
                print(f"Record with {primary_key_field}={primary_key_value} already exists in {table_name}, skipping...")
            else:
                # Insert the data if it does not exist
                response = self.db.table(table_name).insert(record).execute()

                if response.status == 201 or response.data:
                    print(f"Successfully inserted data into {table_name}")
                else:
                    print(f"Failed to insert data into {table_name}: {response.error}")

    def bulk_insert(self, essential_files, other_files):
        # Define the mapping of CSV file paths to their corresponding table names and primary keys
        file_to_table_map = {
            'leagues.csv': ('leagues', 'league_id'),
            'teams.csv': ('teams', 'team_id'),
            'players.csv': ('players', 'player_id'),
            'Bundesliga_Squad_Advanced_Goalkeeping_cleaned.csv': ('team_advanced_goalkeeping', 'stat_id'),
            'Bundesliga_Squad_Defensive_Actions_cleaned.csv': ('team_defensive_actions', 'stat_id'),
            'Bundesliga_Squad_Goal_and_Shot_Creation_cleaned.csv': ('team_goal_and_shot_creation', 'stat_id'),
            'Bundesliga_Squad_Goalkeeping_cleaned.csv': ('team_goalkeeping', 'stat_id'),
            'Bundesliga_Squad_Miscellaneous_Stats_cleaned.csv': ('team_miscellaneous_stats', 'stat_id'),
            'Bundesliga_Squad_Pass_Types_cleaned.csv': ('team_pass_types', 'stat_id'),
            'Bundesliga_Squad_Passing_cleaned.csv': ('team_passing', 'stat_id'),
            'Bundesliga_Squad_Playing_Time_cleaned.csv': ('team_playing_time', 'stat_id'),
            'Bundesliga_Squad_Possession_cleaned.csv': ('team_possession', 'stat_id'),
            'Bundesliga_Squad_Shooting_cleaned.csv': ('team_shooting', 'stat_id'),
            'Bundesliga_Squad_Standard_Stats_cleaned.csv': ('team_standard_stats', 'stat_id'),
            'Defense_cleaned.csv': ('player_defensive_actions', 'stat_id'),
            'Gca_cleaned.csv': ('player_goal_and_shot_creation', 'stat_id'),
            'Keeper_Adv_cleaned.csv': ('player_goalkeeping', 'stat_id'),
            'Keeper_cleaned.csv': ('player_goalkeeping', 'stat_id'),
            'Misc_cleaned.csv': ('player_miscellaneous_stats', 'stat_id'),
            'Passing_cleaned.csv': ('player_passing', 'stat_id'),
            'Passing_Types_cleaned.csv': ('player_pass_types', 'stat_id'),
            'Playing_Time_cleaned.csv': ('player_playing_time', 'stat_id'),
            'Possession_cleaned.csv': ('player_possession', 'stat_id'),
            'Shooting_cleaned.csv': ('player_shooting', 'stat_id'),
            'Standard_cleaned.csv': ('player_standard_stats', 'stat_id'),
        }

        # Insert essential files first (leagues, teams, players)
        essential_files_order = ['leagues.csv', 'teams.csv', 'players.csv']
        for essential_file in essential_files_order:
            essential_path = os.path.join(r"C:\Users\asus\Desktop\Football_project\final_data\First_Tables", essential_file)
            if essential_file in file_to_table_map:
                table_name, primary_key_field = file_to_table_map[essential_file]
                print(f"Inserting {essential_file} into {table_name}")
                self.insert_csv_to_table(essential_path, table_name, primary_key_field)
            else:
                print(f"No table mapping found for {essential_file}")

        # Insert other league data into their respective tables after essential files
        league_directories = [
            r"C:\Users\asus\Desktop\Football_project\final_data\Bundesliga",
            r"C:\Users\asus\Desktop\Football_project\final_data\Premier_League",
            r"C:\Users\asus\Desktop\Football_project\final_data\Serie_A",
            r"C:\Users\asus\Desktop\Football_project\final_data\La_Liga",
            r"C:\Users\asus\Desktop\Football_project\final_data\Ligue_1",
        ]

        for league_dir in league_directories:
            for other_file in os.listdir(league_dir):
                other_path = os.path.join(league_dir, other_file)
                file_name = os.path.basename(other_file)
                if file_name in file_to_table_map:
                    table_name, primary_key_field = file_to_table_map[file_name]
                    print(f"Inserting {file_name} from {league_dir} into {table_name}")
                    self.insert_csv_to_table(other_path, table_name, primary_key_field)
                else:
                    print(f"No table mapping found for {file_name}")
