import os
import pandas as pd
import re

class PlayerDataCleaner:
    def __init__(self, players_data_folder, cleaned_data_folder):
        self.players_data_folder = players_data_folder
        self.cleaned_data_folder = cleaned_data_folder

    def clean_standard_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Standard.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            # Identify the rows where column headers are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index

            # Drop the duplicated rows
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Define the columns to keep
            columns_to_keep = [
                'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', 'MP', 'Starts', 'Min', '90s',
                'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR',
                'xG', 'npxG', 'xAG', 'npxG+xAG', 'PrgC', 'PrgP', 'PrgR',
                'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG'
            ]

            # Keep only the defined columns
            df = df.loc[:, df.columns.intersection(columns_to_keep)]

            # Remove the 'Matches' column
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Identify and rename columns that are under "Per 90 Minutes"
            per_90_columns = [
                'Gls', 'Ast', 'G+A', 'G-PK', 'G+A-PK', 'xG', 'xAG', 'xG+xAG', 'npxG', 'npxG+xAG'
            ]
            for col in per_90_columns:
                # Check if there are multiple columns with the same name
                col_indices = [i for i, c in enumerate(df.columns) if c == col]
                # Rename columns from the second occurrence onwards
                if len(col_indices) > 1:
                    for idx in col_indices[1:]:
                        df.columns.values[idx] = f"{col}_per_90"

            # Convert all columns except 'Player', 'Nation', 'Pos', and 'Squad' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Standard_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_keeper_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Keeper.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            # Identify the rows where column headers are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index

            # Drop the duplicated rows
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Remove the 'Matches' column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Identify and rename columns that are under "Penalty Kicks"
            penalty_columns = ['Att', 'Allowed', 'Saved', 'Missed', 'Save%']
            for col in penalty_columns:
                # Check if the column exists and rename it to avoid conflicts
                col_indices = [i for i, c in enumerate(df.columns) if c == col]
                for idx in col_indices:
                    df.columns.values[idx] = f"{col}_penalty"

            # Convert all columns except 'Player', 'Nation', 'Pos', and 'Squad' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad') with empty strings
            df = df.fillna(0)

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Keeper_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")

    def clean_keeper_adv_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Keeper_Adv.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns but preserve the first level to identify "Goal Kicks"
            level_1 = df.columns.get_level_values(0)  # Level 1 headers
            level_2 = df.columns.get_level_values(1)  # Level 2 headers
            
            # Create new column names based on level 1 and 2 values
            new_columns = []
            for i in range(len(level_1)):
                if level_1[i] == "Goal Kicks":
                    # Rename columns that are under "Goal Kicks" only
                    new_columns.append(f"{level_2[i]}_kicks")
                else:
                    # Keep other columns unchanged
                    new_columns.append(level_2[i])

            # Set the new column names
            df.columns = new_columns

            # Remove the 'Matches' column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', and 'Squad' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Keeper_Adv_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_shooting_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Shooting.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Remove the 'Matches' column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', and 'Squad' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Shooting_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_passing_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Passing.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

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

            # Drop the "Matches" column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', and 'Squad' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Passing_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_passing_types_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Passing_Types.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Drop the "Matches" column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', and 'Squad' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Passing_Types_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
            
    def clean_gca_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Gca.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and rename based on the first level
            new_columns = []
            for level_0, level_1 in df.columns:
                if level_0 == 'SCA Types':
                    new_columns.append(f"{level_1}_sca")
                elif level_0 == 'GCA Types':
                    new_columns.append(f"{level_1}_gca")
                else:
                    new_columns.append(level_1)
            df.columns = new_columns

            # Drop the "Matches" column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', 'Squad' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Gca_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
    
    def clean_defense_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Defense.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and rename based on the first level
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

            # Drop the "Matches" column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', 'Squad', 'Age' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Defense_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_possession_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Possession.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Drop the "Matches" column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', 'Squad', 'Age' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Possession_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_playing_time_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Playing_Time.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Drop the "Matches" column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Drop the "On-Off" columns if they exist
            df = df.drop(columns=[col for col in df.columns if col == 'On-Off'], errors='ignore')

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', 'Squad', 'Age' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Playing_Time_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")
            
    def clean_misc_stats(self):
        leagues = ['Bundesliga', 'Premier_League', 'Serie_A', 'La_Liga', 'Ligue_1']
        
        for league in leagues:
            league_path = os.path.join(self.players_data_folder, league, "Misc.csv")
            
            if not os.path.exists(league_path):
                print(f"File {league_path} does not exist. Skipping this league.")
                continue
            
            # Read the CSV into a DataFrame with multi-level headers
            df = pd.read_csv(league_path, header=[0, 1])
            
            # Remove duplicated rows where column names are repeated
            column_headers = df.columns.get_level_values(1).tolist()
            duplicated_rows = df[df.apply(lambda row: row.tolist() == column_headers, axis=1)].index
            df = df.drop(duplicated_rows)

            # Flatten multi-level columns and keep only the second level
            df.columns = df.columns.get_level_values(1)

            # Drop the "Matches" column if it exists
            if 'Matches' in df.columns:
                df = df.drop(columns=['Matches'])

            # Handle the "Age" column to keep only the part before "-"
            if 'Age' in df.columns:
                df['Age'] = df['Age'].apply(lambda x: re.split(r'[-]', str(x))[0] if pd.notnull(x) else x)

            # Handle the "Nation" column to keep only the characters after the space
            if 'Nation' in df.columns:
                df['Nation'] = df['Nation'].apply(lambda x: x.split()[-1] if pd.notnull(x) and ' ' in x else x)

            # Convert all columns except 'Player', 'Nation', 'Pos', 'Squad', 'Age' to numeric
            for column in df.columns:
                if column not in ['Player', 'Nation', 'Pos', 'Squad', 'Age']:  # These columns should remain as strings
                    try:
                        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)  # Convert to numeric and replace NaN with 0
                    except Exception as e:
                        print(f"Error converting column {column} in {league}: {e}")

            # Replace any remaining NaN values in string columns (e.g., 'Player', 'Nation', 'Pos', 'Squad', 'Age') with empty strings
            df = df.fillna('')

            # Save the cleaned DataFrame to a new CSV file
            save_path = os.path.join(self.cleaned_data_folder, league)
            os.makedirs(save_path, exist_ok=True)
            cleaned_file_path = os.path.join(save_path, "Misc_cleaned.csv")
            df.to_csv(cleaned_file_path, index=False)
            print(f"Cleaned data saved to {cleaned_file_path}")