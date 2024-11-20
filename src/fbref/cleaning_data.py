import os
import pandas as pd

class DataCleaner:
    def __init__(self, data_folder, cleaned_data_folder):
        self.data_folder = data_folder
        self.cleaned_data_folder = cleaned_data_folder

    def clean_squad_standard_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Standard_Stats.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Define the columns to keep
            columns_to_keep = [
                'Squad', '# Pl', 'Age', 'Poss', 'MP', 'Starts', 'Min', '90s',
                'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR',
                'xG', 'npxG', 'xAG', 'npxG+xAG', 'PrgC', 'PrgP',
                'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG'
            ]

            # Ensure we keep the columns in the correct order and drop any not listed
            df = df.loc[:, df.columns.intersection(columns_to_keep)]

            # Identify and rename columns that are under "Per 90 Minutes"
            per_90_columns = ['Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG']
            for col in per_90_columns:
                # Check if there are multiple columns with the same name
                col_indices = [i for i, c in enumerate(df.columns) if c == col]
                # Rename columns from the second occurrence onwards
                if len(col_indices) > 1:
                    for idx in col_indices[1:]:
                        df.columns.values[idx] = f"{col}_per_90"

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # 'Squad' should remain as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Standard_Stats_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")

    def clean_squad_goalkeeping_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Goalkeeping.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Define the columns to keep, removing those under "penalty kicks"
            columns_to_keep = [
                'Squad', '# Pl', 'MP', 'Starts', 'Min', '90s', 'GA', 'GA90', 
                'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS', 'CS%'
            ]

            # Ensure we keep the columns in the correct order and drop any not listed
            df = df.loc[:, df.columns.intersection(columns_to_keep)]

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Goalkeeping_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")

    def clean_squad_advanced_goalkeeping_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Advanced_Goalkeeping.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Identify columns under the "Goal Kicks" category
            columns_to_remove = [col for col in df.columns if col[0] == 'Goal Kicks' and col[1] in ['Att', 'Launch%', 'AvgLen']]

            # Remove only the identified columns under "Goal Kicks"
            df = df.drop(columns=columns_to_remove, errors='ignore')

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Advanced_Goalkeeping_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")

    def clean_squad_shooting_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Shooting.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Shooting_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_squad_passing_stats(self):
            leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
            
            for league in leagues:
                league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Passing.csv")
                
                if not os.path.exists(league_path):
                    print(f"File {league_path} does not exist. Skipping this league.")
                    continue
                
                # Read the CSV into a DataFrame with multi-level headers
                df = pd.read_csv(league_path, header=[0, 1])

                # Create a new list for the column names
                new_columns = []

                # Iterate over multi-level column names
                for level_1, level_2 in df.columns:
                    # Rename based on the level 1 column name
                    if level_1 == 'Total':
                        new_columns.append(f"{level_2}_total")
                    elif level_1 == 'Short':
                        new_columns.append(f"{level_2}_short")
                    elif level_1 == 'Medium':
                        new_columns.append(f"{level_2}_medium")
                    elif level_1 == 'Long':
                        new_columns.append(f"{level_2}_long")
                    else:
                        # Keep other columns as they are
                        new_columns.append(level_2)

                # Assign the new column names to the DataFrame
                df.columns = new_columns

                # Convert all columns except 'Squad' to numeric
                for column in df.columns:
                    if column != 'Squad':  # Ensure 'Squad' remains as a string
                        try:
                            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                        except Exception as e:
                            print(f"Error converting column {column} in {league}: {e}")

                # Save the cleaned DataFrame to a new CSV file
                save_path = os.path.join(self.cleaned_data_folder, league)
                os.makedirs(save_path, exist_ok=True)
                cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Passing_cleaned.csv")
                df.to_csv(cleaned_file_path, index=False)
                print(f"Cleaned data saved to {cleaned_file_path}")
                
    def clean_squad_pass_types_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Pass_Types.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Pass_Types_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_squad_goal_and_shot_creation_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Goal_and_Shot_Creation.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns
            new_columns = []
            for level_0, level_1 in df.columns:
                if level_0 == 'SCA Types':
                    new_columns.append(f"{level_1}_sca")
                elif level_0 == 'GCA Types':
                    new_columns.append(f"{level_1}_gca")
                else:
                    new_columns.append(level_1)
            df.columns = new_columns

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Goal_and_Shot_Creation_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_squad_defensive_actions_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Defensive_Actions.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns
            new_columns = []
            for level_0, level_1 in df.columns:
                if level_0 == 'Tackles':
                    new_columns.append(f"{level_1}_tackles")
                elif level_0 == 'Challenges':
                    new_columns.append(f"{level_1}_challenges")
                elif level_0 == 'Blocks':
                    new_columns.append(f"{level_1}_blocks")
                else:
                    new_columns.append(level_1)
            df.columns = new_columns

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Defensive_Actions_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_squad_possession_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Possession.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Possession_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_squad_playing_time_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Playing_Time.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Playing_Time_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_squad_miscellaneous_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.data_folder, league, f"{league}_Squad_Miscellaneous_Stats.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Convert all columns except 'Squad' to numeric
            for column in df.columns:
                if column != 'Squad':  # Ensure 'Squad' remains as a string
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, f"{league}_Squad_Miscellaneous_Stats_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
