import os
import pandas as pd

class FinalDataTransformation:
    def __init__(self):
        # Directories for input data
        self.input_dirs = {
            'Bundesliga': r'C:/Users/asus/Desktop/Football_project/cleaned_data/Bundesliga',
            'La_Liga': r'C:/Users/asus/Desktop/Football_project/cleaned_data/La_Liga',
            'Ligue_1': r'C:/Users/asus/Desktop/Football_project/cleaned_data/Ligue_1',
            'Premier_League': r'C:/Users/asus/Desktop/Football_project/cleaned_data/Premier_League',
            'Serie_A': r'C:/Users/asus/Desktop/Football_project/cleaned_data/Serie_A',
            'First_Tables': r'C:/Users/asus/Desktop/Football_project/first_tables'
        }

        # Directory for final output
        self.output_dir = r'C:/Users/asus/Desktop/Football_project/final_data'

        # Ensure final output folders exist for each league
        self._create_output_directories()
        
        self.teams_df = pd.read_csv(r"C:\Users\asus\Desktop\Football_project\final_data\First_Tables\teams.csv")
        
    def _get_team_id(self, team_name):
        # Match the team_name in the 'teams_df' and return the corresponding team_id
        team_row = self.teams_df[self.teams_df['team_name'] == team_name]
        if not team_row.empty:
            return team_row.iloc[0]['team_id']
        return None

    def _create_output_directories(self):
        """Create output directories for each league in the final_data folder."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        for league in self.input_dirs.keys():
            league_output_dir = os.path.join(self.output_dir, league)
            if not os.path.exists(league_output_dir):
                os.makedirs(league_output_dir)

    def transform_and_save(self):
        """Run transformations and save each CSV into its respective folder."""
        for league, input_dir in self.input_dirs.items():
            # Skip the 'First_Tables' directory since it doesn't have Standard_cleaned.csv
            if league == 'First_Tables':
                continue
            
            self._process_league(league, input_dir)

    def _process_league(self, league, input_dir):
        """Process all files in a league's folder and apply transformations."""
        files = os.listdir(input_dir)
        
        # Get the league file path for player-team mapping from the cleaned data folder
        league_file_path = os.path.join(input_dir, "Standard_cleaned.csv")
        
        if not os.path.exists(league_file_path):
            print(f"Error: {league_file_path} does not exist.")
            return  # Skip processing this league if the file does not exist
        
        for file in files:
            file_path = os.path.join(input_dir, file)
            if file.endswith('.csv'):
                df = pd.read_csv(file_path)
                
                # Match file type to the correct transformation function
                
                # First Tables
                if 'leagues' in file:
                    df = self._transform_leagues(df)
                elif 'teams' in file:
                    df = self._transform_teams(df)
                elif 'players' in file:
                    df = self._transform_players(df, league_file_path)  # Pass the correct league_file_path here
                
                # Non-squad league data
                elif 'Keeper_Adv' in file:
                    df = self._transform_advanced_goalkeeping(df)
                elif 'Defense' in file and 'Squad' not in file:
                    df = self._transform_defensive_actions(df)
                elif 'Gca' in file and 'Squad' not in file:
                    df = self._transform_goal_and_shot_creation(df)
                elif 'Keeper' in file and 'Adv' not in file and 'Squad' not in file:
                    df = self._transform_goalkeeping(df)
                elif 'Misc_cleaned' in file and 'Squad' not in file:
                    df = self._transform_miscellaneous_stats(df)
                elif 'Passing_Types' in file and 'Squad' not in file:
                    df = self._transform_pass_types(df)
                elif 'Passing_cleaned' in file and 'Squad' not in file:
                    df = self._transform_passing(df)
                elif 'Playing_Time' in file and 'Squad' not in file:
                    df = self._transform_playing_time(df)
                elif 'Possession' in file and 'Squad' not in file:
                    df = self._transform_possession(df)
                elif 'Shooting' in file and 'Squad' not in file:
                    df = self._transform_shooting(df)
                elif 'Standard' in file and 'Squad' not in file:
                    df = self._transform_standard_stats(df)
                
                # Squad data
                elif 'Squad_Advanced_Goalkeeping' in file:
                    df = self._transform_team_advanced_goalkeeping(df)
                elif 'Squad_Defensive_Actions' in file:
                    df = self._transform_team_defensive_actions(df)
                elif 'Squad_Goal_and_Shot_Creation' in file:
                    df = self._transform_team_goal_and_shot_creation(df)
                elif 'Squad_Goalkeeping' in file:
                    df = self._transform_team_goalkeeping(df)
                elif 'Squad_Miscellaneous_Stats' in file:
                    df = self._transform_team_miscellaneous_stats(df)
                elif 'Squad_Pass_Types' in file:
                    df = self._transform_team_pass_types(df)
                elif 'Squad_Passing' in file and 'Pass_Types' not in file:
                    df = self._transform_team_passing(df)
                elif 'Squad_Playing_Time' in file:
                    df = self._transform_team_playing_time(df)
                elif 'Squad_Possession' in file:
                    df = self._transform_team_possession(df)
                elif 'Squad_Shooting' in file:
                    df = self._transform_team_shooting(df)
                elif 'Squad_Standard_Stats' in file:
                    df = self._transform_team_standard_stats(df)
                
                # Save transformed DataFrame
                self._save_transformed_data(df, league, file)

    def _save_transformed_data(self, df, league, filename):
        """Save the transformed DataFrame to the respective league folder."""
        league_output_dir = os.path.join(self.output_dir, league)
        output_path = os.path.join(league_output_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"Saved transformed file to {output_path}")

    def _transform_leagues(self, df):
        """Transform the Leagues data to match the schema."""
        df.rename(columns={
            'ID': 'league_id',  # Rename 'ID' to 'league_id'
            'league_name': 'league_name'
        }, inplace=True)
        
        return df[['league_id', 'league_name']].astype({'league_id': 'int'})  # Ensure correct column order and data type


    def _transform_teams(self, df):
        """Transform the Teams data to match the schema."""
        
        # Create a dictionary to map teams to their respective league_id
        league_mapping = {
            1: ['Augsburg', 'Bayern Munich', 'Bochum', 'Dortmund', 'Eint Frankfurt', 'Freiburg', 'Gladbach', 
                'Heidenheim', 'Hoffenheim', 'Holstein Kiel', 'Leverkusen', 'Mainz 05', 'RB Leipzig', 
                'St. Pauli', 'Stuttgart', 'Union Berlin', 'Werder Bremen', 'Wolfsburg'],
            2: ['Alavés', 'Athletic Club', 'Atlético Madrid', 'Barcelona', 'Betis', 'Celta Vigo', 'Espanyol', 
                'Getafe', 'Girona', 'Las Palmas', 'Leganés', 'Mallorca', 'Osasuna', 'Rayo Vallecano', 
                'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Valladolid', 'Villarreal'],
            3: ['Angers', 'Auxerre', 'Brest', 'Le Havre', 'Lens', 'Lille', 'Lyon', 'Marseille', 'Monaco', 
                'Montpellier', 'Nantes', 'Nice', 'Paris S-G', 'Reims', 'Rennes', 'Saint-Étienne', 
                'Strasbourg', 'Toulouse'],
            4: ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Chelsea', 'Crystal Palace', 
                'Everton', 'Fulham', 'Ipswich Town', 'Leicester City', 'Liverpool', 'Manchester City', 
                'Manchester Utd', 'Newcastle Utd', 'Nott\'ham Forest', 'Southampton', 'Tottenham', 
                'West Ham', 'Wolves'],
            5: ['Atalanta', 'Bologna', 'Cagliari', 'Como', 'Empoli', 'Fiorentina', 'Genoa', 'Hellas Verona', 
                'Inter', 'Juventus', 'Lazio', 'Lecce', 'Milan', 'Monza', 'Napoli', 'Parma', 'Roma', 
                'Torino', 'Udinese', 'Venezia']
        }

        # Initialize the team_id as an empty list
        df['team_id'] = range(1, len(df) + 1)  # Generating unique team_id
        
        # Map the league_id based on team name
        def get_league_id(team_name):
            for league_id, teams in league_mapping.items():
                if team_name in teams:
                    return league_id
            return None  # If no match, return None

        df['league_id'] = df['team_name'].apply(get_league_id)

        # Ensure the columns are in the correct order and the right data types
        df = df[['team_id', 'team_name', 'league_id']].astype({
            'team_id': 'int64',
            'league_id': 'int64',
            'team_name': 'string'
        })

        return df

    def _transform_players(self, df, league_file_path):
        """Transform the Players data to match the schema."""
        
        # Load the teams.csv to get the team_name and team_id mapping
        teams_df = pd.read_csv(r"C:\Users\asus\Desktop\Football_project\final_data\First_Tables\teams.csv")
        
        # Load the league data that contains the 'Squad' (team_name) and 'Player' (player_name)
        league_df = pd.read_csv(league_file_path)
        
        # Merge the teams dataframe with league dataframe based on 'Squad' column from league and 'team_name' from teams
        merged_df = pd.merge(df, league_df[['Player', 'Squad']], left_on='player_name', right_on='Player', how='left')
        
        # Merge again to assign team_id from teams.csv based on the Squad (team_name)
        merged_df = pd.merge(merged_df, teams_df[['team_id', 'team_name']], left_on='Squad', right_on='team_name', how='left')
        
        # Drop unnecessary columns
        merged_df.drop(columns=['Player', 'Squad', 'team_name'], inplace=True)

        # Rename columns to match the schema
        merged_df.rename(columns={
            'player_name': 'player_name',
            'nation': 'nation',
            'position': 'position',
            'age': 'age',
            'date_of_birth': 'date_of_birth',
            'team_id': 'team_id'
        }, inplace=True)

        # Add 'player_id' column, initialized with None
        merged_df['player_id'] = None

        # Reorder the columns: player_id, player_name, nation, position, team_id, age, date_of_birth
        merged_df = merged_df[['player_id', 'player_name', 'nation', 'position', 'team_id', 'age', 'date_of_birth']]

        # Set correct data types
        merged_df = merged_df.astype({
            'player_id': 'Int64',  # Nullable integer for player_id
            'team_id': 'Int64',    # Nullable integer for team_id
            'age': 'int',
            'date_of_birth': 'float'  # For proper date formatting, can be updated if required
        })

        return merged_df

    def _transform_advanced_goalkeeping(self, df):
        """Transform the Advanced Goalkeeping data to match the schema."""
        # Drop the columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True, errors='ignore')

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be generated or filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'GA': 'ga',
            'PKA': 'pka',
            'FK': 'fk',
            'CK': 'ck',
            'OG': 'og',
            'PSxG': 'psxg',
            'PSxG/SoT': 'psxg_per_sot',
            'PSxG+/-': 'psxg_plus_minus',
            '/90': 'psxg_plus_minus_per_90',
            'Cmp': 'cmp',
            'Att': 'att',
            'Cmp%': 'cmp_percent',
            'Att (GK)': 'att_gk',
            'Thr': 'thr',
            'Launch%': 'launch_percent',
            'AvgLen': 'avg_len',
            'Opp': 'opp',
            'Stp': 'stp',
            'Stp%': 'stp_percent',
            '#OPA': 'opa',
            '#OPA/90': 'opa_per_90',
            'AvgDist': 'avg_dist'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'ga', 'pka', 'fk', 'ck', 'og', 'psxg', 'psxg_per_sot',
                'psxg_plus_minus', 'psxg_plus_minus_per_90', 'cmp', 'att', 'cmp_percent', 'att_gk', 'thr',
                'launch_percent', 'avg_len', 'opp', 'stp', 'stp_percent', 'opa', 'opa_per_90', 'avg_dist']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'ga': 'int',
            'pka': 'int',
            'fk': 'int',
            'ck': 'int',
            'og': 'int',
            'psxg': 'float',
            'psxg_per_sot': 'float',
            'psxg_plus_minus': 'float',
            'psxg_plus_minus_per_90': 'float',
            'cmp': 'int',
            'att': 'int',
            'cmp_percent': 'float',
            'att_gk': 'int',
            'thr': 'int',
            'launch_percent': 'float',
            'avg_len': 'float',
            'opp': 'int',
            'stp': 'int',
            'stp_percent': 'float',
            'opa': 'int',
            'opa_per_90': 'float',
            'avg_dist': 'float'
        })

                   
    def _transform_defensive_actions(self, df):
        """Transform the Defensive Actions data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Tkl_tackles': 'tkl_tackles',
            'TklW_tackles': 'tklw_tackles',
            'Def 3rd_tackles': 'def_3rd_tackles',
            'Mid 3rd_tackles': 'mid_3rd_tackles',
            'Att 3rd_tackles': 'att_3rd_tackles',
            'Tkl_challenges': 'tkl_challenges',
            'Att_challenges': 'att_challenges',
            'Tkl%_challenges': 'tkl_percent_challenges',
            'Lost_challenges': 'lost_challenges',
            'Blocks_blocks': 'blocks_blocks',
            'Sh_blocks': 'sh_blocks',
            'Pass_blocks': 'pass_blocks',
            'Int': 'interceptions',
            'Tkl+Int': 'tkl_plus_int',
            'Clr': 'clr',
            'Err': 'err'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'tkl_tackles', 'tklw_tackles', 'def_3rd_tackles', 'mid_3rd_tackles', 
                'att_3rd_tackles', 'tkl_challenges', 'att_challenges', 'tkl_percent_challenges', 'lost_challenges', 
                'blocks_blocks', 'sh_blocks', 'pass_blocks', 'interceptions', 'tkl_plus_int', 'clr', 'err']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'tkl_tackles': 'int',
            'tklw_tackles': 'int',
            'def_3rd_tackles': 'int',
            'mid_3rd_tackles': 'int',
            'att_3rd_tackles': 'int',
            'tkl_challenges': 'int',
            'att_challenges': 'int',
            'tkl_percent_challenges': 'float',
            'lost_challenges': 'int',
            'blocks_blocks': 'int',
            'sh_blocks': 'int',
            'pass_blocks': 'int',
            'interceptions': 'int',
            'tkl_plus_int': 'int',
            'clr': 'int',
            'err': 'int'
        })
    
    def _transform_goal_and_shot_creation(self, df):
        """Transform the Goal and Shot Creation data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'SCA': 'sca',
            'SCA90': 'sca_per_90',
            'PassLive_sca': 'passlive_sca',
            'PassDead_sca': 'passdead_sca',
            'TO_sca': 'to_sca',
            'Sh_sca': 'sh_sca',
            'Fld_sca': 'fld_sca',
            'Def_sca': 'def_sca',
            'GCA': 'gca',
            'GCA90': 'gca_per_90',
            'PassLive_gca': 'passlive_gca',
            'PassDead_gca': 'passdead_gca',
            'TO_gca': 'to_gca',
            'Sh_gca': 'sh_gca',
            'Fld_gca': 'fld_gca',
            'Def_gca': 'def_gca'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'sca', 'sca_per_90', 'passlive_sca', 'passdead_sca', 'to_sca', 
                'sh_sca', 'fld_sca', 'def_sca', 'gca', 'gca_per_90', 'passlive_gca', 'passdead_gca', 'to_gca', 
                'sh_gca', 'fld_gca', 'def_gca']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'sca': 'int',
            'sca_per_90': 'float',
            'passlive_sca': 'int',
            'passdead_sca': 'int',
            'to_sca': 'int',
            'sh_sca': 'int',
            'fld_sca': 'int',
            'def_sca': 'int',
            'gca': 'int',
            'gca_per_90': 'float',
            'passlive_gca': 'int',
            'passdead_gca': 'int',
            'to_gca': 'int',
            'sh_gca': 'int',
            'fld_gca': 'int',
            'def_gca': 'int'
        })

    def _transform_goalkeeping(self, df):
        """Transform the Goalkeeping data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            'MP': 'mp',
            'Starts': 'starts',
            'Min': 'min',
            '90s': 'ninety_s',
            'GA': 'ga',
            'GA90': 'ga_per_90',
            'SoTA': 'sota',
            'Saves': 'saves',
            'Save%_penalty': 'save_percent',
            'W': 'w',
            'D': 'd',
            'L': 'l',
            'CS': 'cs',
            'CS%': 'cs_percent',
            'PKatt': 'pkatt',
            'PKA': 'pka',
            'PKsv': 'pk_sv',
            'PKm': 'pk_missed'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'mp', 'starts', 'min', 'ninety_s', 'ga', 'ga_per_90', 'sota', 'saves', 
                'save_percent', 'w', 'd', 'l', 'cs', 'cs_percent', 'pkatt', 'pka', 'pk_sv', 'pk_missed']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'mp': 'int',
            'starts': 'int',
            'min': 'int',
            'ninety_s': 'float',
            'ga': 'int',
            'ga_per_90': 'float',
            'sota': 'int',
            'saves': 'int',
            'save_percent': 'float',
            'w': 'int',
            'd': 'int',
            'l': 'int',
            'cs': 'int',
            'cs_percent': 'float',
            'pkatt': 'int',
            'pka': 'int',
            'pk_sv': 'int',
            'pk_missed': 'int'
        })

    def _transform_miscellaneous_stats(self, df):
        """Transform the Miscellaneous Stats data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'CrdY': 'crd_y',
            'CrdR': 'crd_r',
            '2CrdY': 'two_crd_y',
            'Fls': 'fls',
            'Fld': 'fld',
            'Off': 'off',
            'Crs': 'crs',
            'Int': 'interceptions',
            'TklW': 'tklw',
            'PKwon': 'pkwon',
            'PKcon': 'pkcon',
            'OG': 'og',
            'Recov': 'recov',
            'Won': 'won',
            'Lost': 'lost',
            'Won%': 'won_percent'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'crd_y', 'crd_r', 'two_crd_y', 'fls', 'fld', 'off', 'crs', 
                'interceptions', 'tklw', 'pkwon', 'pkcon', 'og', 'recov', 'won', 'lost', 'won_percent']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'crd_y': 'int',
            'crd_r': 'int',
            'two_crd_y': 'int',
            'fls': 'int',
            'fld': 'int',
            'off': 'int',
            'crs': 'int',
            'interceptions': 'int',
            'tklw': 'int',
            'pkwon': 'int',
            'pkcon': 'int',
            'og': 'int',
            'recov': 'int',
            'won': 'int',
            'lost': 'int',
            'won_percent': 'float'
        })
    
    def _transform_pass_types(self, df):
        """Transform the Pass Types data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Att': 'att',
            'Live': 'live',
            'Dead': 'dead',
            'FK': 'fk',
            'TB': 'tb',
            'Sw': 'sw',
            'Crs': 'crs',
            'TI': 'ti',
            'CK': 'ck',
            'In': 'inn',
            'Out': 'outt',
            'Str': 'str',
            'Cmp': 'cmp',
            'Off': 'off',
            'Blocks': 'blocks'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'att', 'live', 'dead', 'fk', 'tb', 'sw', 'crs', 'ti', 'ck', 
                'inn', 'outt', 'str', 'cmp', 'off', 'blocks']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'att': 'int',
            'live': 'int',
            'dead': 'int',
            'fk': 'int',
            'tb': 'int',
            'sw': 'int',
            'crs': 'int',
            'ti': 'int',
            'ck': 'int',
            'inn': 'int',
            'outt': 'int',
            'str': 'int',
            'cmp': 'int',
            'off': 'int',
            'blocks': 'int'
        })

    def _transform_passing(self, df):
        """Transform the Passing data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True, errors='ignore')

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Cmp_total': 'cmp_total',
            'Att_total': 'att_total',
            'Cmp%_total': 'cmp_percent_total',
            'TotDist_total': 'tot_dist_total',
            'PrgDist_total': 'prg_dist_total',
            'Cmp_short': 'cmp_short',
            'Att_short': 'att_short',
            'Cmp%_short': 'cmp_percent_short',
            'Cmp_medium': 'cmp_medium',
            'Att_medium': 'att_medium',
            'Cmp%_medium': 'cmp_percent_medium',
            'Cmp_long': 'cmp_long',
            'Att_long': 'att_long',
            'Cmp%_long': 'cmp_percent_long',
            'Ast': 'ast',
            'xAG': 'xag',
            'xA': 'xa',
            'A-xAG': 'a_xag',  # This was corrected from 'a_xag' to 'A-xAG'
            'KP': 'kp',
            '1/3': 'one_third_ppa',
            'CrsPA': 'crspa',
            'PrgP': 'prgp'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'cmp_total', 'att_total', 'cmp_percent_total', 'tot_dist_total',
                'prg_dist_total', 'cmp_short', 'att_short', 'cmp_percent_short', 'cmp_medium', 'att_medium',
                'cmp_percent_medium', 'cmp_long', 'att_long', 'cmp_percent_long', 'ast', 'xa', 'xag', 'a_xag', 'kp',
                'one_third_ppa', 'crspa', 'prgp']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'cmp_total': 'int',
            'att_total': 'int',
            'cmp_percent_total': 'float',
            'tot_dist_total': 'float',
            'prg_dist_total': 'float',
            'cmp_short': 'int',
            'att_short': 'int',
            'cmp_percent_short': 'float',
            'cmp_medium': 'int',
            'att_medium': 'int',
            'cmp_percent_medium': 'float',
            'cmp_long': 'int',
            'att_long': 'int',
            'cmp_percent_long': 'float',
            'ast': 'int',
            'xa': 'float',
            'xag': 'float',
            'a_xag': 'float',  # Corrected here
            'kp': 'int',
            'one_third_ppa': 'int',
            'crspa': 'int',
            'prgp': 'int'
        })

    def _transform_playing_time(self, df):
        """Transform the Playing Time data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            'MP': 'mp',
            'Min': 'min',
            '90s': 'ninety_s',
            'Starts': 'starts',
            'Mn/Start': 'mn_per_start',
            'Compl': 'compl',
            'Subs': 'subs',
            'Mn/Sub': 'mn_per_subs',
            'unSub': 'unsub',
            'PPM': 'ppm',
            'onG': 'on_g',
            'onGA': 'on_ga',
            '+/-': 'plus_minus',
            '+/-90': 'plus_minus_per_90',
            'onxG': 'onxg',
            'onxGA': 'onxga',
            'xG+/-': 'xg_plus_minus',
            'xG+/-90': 'xg_plus_minus_per_90'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'mp', 'min', 'ninety_s', 'starts', 'mn_per_start', 'compl', 'subs', 
                'mn_per_subs', 'unsub', 'ppm', 'on_g', 'on_ga', 'plus_minus', 'plus_minus_per_90', 'onxg', 'onxga', 
                'xg_plus_minus', 'xg_plus_minus_per_90']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'mp': 'int',
            'min': 'int',
            'ninety_s': 'float',
            'starts': 'int',
            'mn_per_start': 'float',
            'compl': 'int',
            'subs': 'int',
            'mn_per_subs': 'float',
            'unsub': 'int',
            'ppm': 'float',
            'on_g': 'int',
            'on_ga': 'int',
            'plus_minus': 'int',
            'plus_minus_per_90': 'float',
            'onxg': 'float',
            'onxga': 'float',
            'xg_plus_minus': 'float',
            'xg_plus_minus_per_90': 'float'
        })

    def _transform_possession(self, df):
        """Transform the Possession data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Touches': 'touches',
            'Def Pen': 'def_pen',
            'Def 3rd': 'def_3rd',
            'Mid 3rd': 'mid_3rd',
            'Att 3rd': 'att_3rd',
            'Att Pen': 'att_pen',
            'Live': 'live',
            'Att': 'att',
            'Succ': 'succ',
            'Succ%': 'succ_percent',
            'Tkld': 'tkld',
            'Tkld%': 'tkld_percent',
            'Carries': 'carries',
            'TotDist': 'tot_dist',
            'PrgDist': 'prg_dist',
            'PrgC': 'prgc',
            '1/3': 'one_third',
            'CPA': 'cpa',
            'Mis': 'mis',
            'Dis': 'dis',
            'Rec': 'rec',
            'PrgR': 'prgr'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'touches', 'def_pen', 'def_3rd', 'mid_3rd', 'att_3rd', 'att_pen', 'live', 
                'att', 'succ', 'succ_percent', 'tkld', 'tkld_percent', 'carries', 'tot_dist', 'prg_dist', 'prgc', 
                'one_third', 'cpa', 'mis', 'dis', 'rec', 'prgr']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'touches': 'int',
            'def_pen': 'int',
            'def_3rd': 'int',
            'mid_3rd': 'int',
            'att_3rd': 'int',
            'att_pen': 'int',
            'live': 'int',
            'att': 'int',
            'succ': 'int',
            'succ_percent': 'float',
            'tkld': 'int',
            'tkld_percent': 'float',
            'carries': 'int',
            'tot_dist': 'float',
            'prg_dist': 'float',
            'prgc': 'int',
            'one_third': 'int',
            'cpa': 'int',
            'mis': 'int',
            'dis': 'int',
            'rec': 'int',
            'prgr': 'int'
        })
                   
    def _transform_shooting(self, df):
        """Transform the Shooting data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Gls': 'gls',
            'Sh': 'sh',
            'SoT': 'sot',
            'SoT%': 'sot_percent',
            'Sh/90': 'sh_per_90',
            'SoT/90': 'sot_per_90',
            'G/Sh': 'g_per_sh',
            'G/SoT': 'g_per_sot',
            'Dist': 'dist',
            'FK': 'fk',
            'PK': 'pk',
            'PKatt': 'pkatt',
            'xG': 'xg',
            'npxG': 'npxg',
            'npxG/Sh': 'npxg_per_sh',
            'G-xG': 'g_minus_xg',
            'np:G-xG': 'npg_minus_xg'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'ninety_s', 'gls', 'sh', 'sot', 'sot_percent', 'sh_per_90', 'sot_per_90', 'g_per_sh', 
                'g_per_sot', 'dist', 'fk', 'pk', 'pkatt', 'xg', 'npxg', 'npxg_per_sh', 'g_minus_xg', 'npg_minus_xg']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'gls': 'int',
            'sh': 'int',
            'sot': 'int',
            'sot_percent': 'float',
            'sh_per_90': 'float',
            'sot_per_90': 'float',
            'g_per_sh': 'float',
            'g_per_sot': 'float',
            'dist': 'float',
            'fk': 'int',
            'pk': 'int',
            'pkatt': 'int',
            'xg': 'float',
            'npxg': 'float',
            'npxg_per_sh': 'float',
            'g_minus_xg': 'float',
            'npg_minus_xg': 'float'
        })

    def _transform_standard_stats(self, df):
        """Transform the Standard Stats data to match the schema."""
        # Drop unnecessary columns: 'Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'
        df.drop(columns=['Rk', 'Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born'], inplace=True)

        # Add new empty columns 'stat_id' and 'player_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['player_id'] = None  # Empty player_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            'MP': 'mp',
            'Min': 'min',
            '90s': 'ninety_s',
            'Starts': 'starts',
            'Gls': 'gls',
            'Gls_per_90': 'gls_per_90',
            'Ast': 'ast',
            'Ast_per_90': 'ast_per_90',
            'G+A': 'g_a',
            'G+A_per_90': 'g_a_per_90',
            'G-PK': 'g_pk',
            'G-PK_per_90': 'g_pk_per_90',
            'PK': 'pk',
            'PKatt': 'pkatt',
            'CrdY': 'crd_y',
            'CrdR': 'crd_r',
            'xG': 'xg',
            'xG_per_90': 'xg_per_90',
            'npxG': 'npxg',
            'npxG_per_90': 'npxg_per_90',
            'xAG': 'xag',
            'xAG_per_90': 'xag_per_90',
            'npxG+xAG': 'npxg_xag',
            'npxG+xAG_per_90': 'npxg_xag_per_90'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'player_id', 'mp', 'min', 'ninety_s', 'starts', 'gls', 'gls_per_90', 'ast', 
                'ast_per_90', 'g_a', 'g_a_per_90', 'g_pk', 'g_pk_per_90', 'pk', 'pkatt', 'crd_y', 'crd_r', 'xg', 
                'xg_per_90', 'npxg', 'npxg_per_90', 'xag', 'xag_per_90', 'npxg_xag', 'npxg_xag_per_90']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'player_id': 'Int64',  # Nullable integer
            'mp': 'int',
            'min': 'int',
            'ninety_s': 'float',
            'starts': 'int',
            'gls': 'int',
            'gls_per_90': 'float',
            'ast': 'int',
            'ast_per_90': 'float',
            'g_a': 'int',
            'g_a_per_90': 'float',
            'g_pk': 'int',
            'g_pk_per_90': 'float',
            'pk': 'int',
            'pkatt': 'int',
            'crd_y': 'int',
            'crd_r': 'int',
            'xg': 'float',
            'xg_per_90': 'float',
            'npxg': 'float',
            'npxg_per_90': 'float',
            'xag': 'float',
            'xag_per_90': 'float',
            'npxg_xag': 'float',
            'npxg_xag_per_90': 'float'
        })


    
    
    
    

    def _transform_team_advanced_goalkeeping(self, df):
        """Transform the Team Advanced Goalkeeping data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'GA': 'ga',
            'PKA': 'pka',
            'FK': 'fk',
            'CK': 'ck',
            'OG': 'og',
            'PSxG': 'psxg',
            'PSxG/SoT': 'psxg_per_sot',
            'PSxG+/-': 'psxg_plus_minus',
            '/90': 'psxg_plus_minus_per_90',
            'Cmp': 'cmp',
            'Att': 'att',
            'Cmp%': 'cmp_percent',
            'Att (GK)': 'att_gk',
            'Thr': 'thr',
            'Launch%': 'launch_percent',
            'AvgLen': 'avg_len',
            'Opp': 'opp',
            'Stp': 'stp',
            'Stp%': 'stp_percent',
            '#OPA': 'opa',
            '#OPA/90': 'opa_per_90',
            'AvgDist': 'avg_dist'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'ga', 'pka', 'fk', 'ck', 'og', 'psxg', 'psxg_per_sot', 'psxg_plus_minus', 
                'psxg_plus_minus_per_90', 'cmp', 'att', 'cmp_percent', 'att_gk', 'thr', 'launch_percent', 'avg_len', 
                'opp', 'stp', 'stp_percent', 'opa', 'opa_per_90', 'avg_dist']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'ga': 'int',
            'pka': 'int',
            'fk': 'int',
            'ck': 'int',
            'og': 'int',
            'psxg': 'float',
            'psxg_per_sot': 'float',
            'psxg_plus_minus': 'float',
            'psxg_plus_minus_per_90': 'float',
            'cmp': 'int',
            'att': 'int',
            'cmp_percent': 'float',
            'att_gk': 'int',
            'thr': 'int',
            'launch_percent': 'float',
            'avg_len': 'float',
            'opp': 'int',
            'stp': 'int',
            'stp_percent': 'float',
            'opa': 'int',
            'opa_per_90': 'float',
            'avg_dist': 'float'
        })

    def _transform_team_defensive_actions(self, df):
        """Transform the Team Defensive Actions data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Tkl_tackles': 'tkl_tackles',
            'TklW_tackles': 'tklw_tackles',
            'Def 3rd_tackles': 'def_3rd_tackles',
            'Mid 3rd_tackles': 'mid_3rd_tackles',
            'Att 3rd_tackles': 'att_3rd_tackles',
            'Tkl_challenges': 'tkl_challenges',
            'Att_challenges': 'att_challenges',
            'Tkl%_challenges': 'tkl_percent_challenges',
            'Lost_challenges': 'lost_challenges',
            'Blocks_blocks': 'blocks_blocks',
            'Sh_blocks': 'sh_blocks',
            'Pass_blocks': 'pass_blocks',
            'Int': 'interceptions',
            'Tkl+Int': 'tkl_plus_int',
            'Clr': 'clr',
            'Err': 'err'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'tkl_tackles', 'tklw_tackles', 'def_3rd_tackles', 'mid_3rd_tackles', 
                'att_3rd_tackles', 'tkl_challenges', 'att_challenges', 'tkl_percent_challenges', 'lost_challenges', 
                'blocks_blocks', 'sh_blocks', 'pass_blocks', 'interceptions', 'tkl_plus_int', 'clr', 'err']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'tkl_tackles': 'int',
            'tklw_tackles': 'int',
            'def_3rd_tackles': 'int',
            'mid_3rd_tackles': 'int',
            'att_3rd_tackles': 'int',
            'tkl_challenges': 'int',
            'att_challenges': 'int',
            'tkl_percent_challenges': 'float',
            'lost_challenges': 'int',
            'blocks_blocks': 'int',
            'sh_blocks': 'int',
            'pass_blocks': 'int',
            'interceptions': 'int',
            'tkl_plus_int': 'int',
            'clr': 'int',
            'err': 'int'
        })

    def _transform_team_goal_and_shot_creation(self, df):
        """Transform the Team Goal and Shot Creation data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'SCA': 'sca',
            'SCA90': 'sca_per_90',
            'PassLive_sca': 'passlive_sca',
            'PassDead_sca': 'passdead_sca',
            'TO_sca': 'to_sca',
            'Sh_sca': 'sh_sca',
            'Fld_sca': 'fld_sca',
            'Def_sca': 'def_sca',
            'GCA': 'gca',
            'GCA90': 'gca_per_90',
            'PassLive_gca': 'passlive_gca',
            'PassDead_gca': 'passdead_gca',
            'TO_gca': 'to_gca',
            'Sh_gca': 'sh_gca',
            'Fld_gca': 'fld_gca',
            'Def_gca': 'def_gca'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'sca', 'sca_per_90', 'passlive_sca', 'passdead_sca', 'to_sca', 
                'sh_sca', 'fld_sca', 'def_sca', 'gca', 'gca_per_90', 'passlive_gca', 'passdead_gca', 'to_gca', 
                'sh_gca', 'fld_gca', 'def_gca']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'sca': 'int',
            'sca_per_90': 'float',
            'passlive_sca': 'int',
            'passdead_sca': 'int',
            'to_sca': 'int',
            'sh_sca': 'int',
            'fld_sca': 'int',
            'def_sca': 'int',
            'gca': 'int',
            'gca_per_90': 'float',
            'passlive_gca': 'int',
            'passdead_gca': 'int',
            'to_gca': 'int',
            'sh_gca': 'int',
            'fld_gca': 'int',
            'def_gca': 'int'
        })

    def _transform_team_goalkeeping(self, df):
        """Transform the Team Goalkeeping data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            'MP': 'mp',
            'Starts': 'starts',
            'Min': 'min',
            '90s': 'ninety_s',
            'GA': 'ga',
            'GA90': 'ga_per_90',
            'SoTA': 'sota',
            'Saves': 'saves',
            'Save%': 'save_percent',
            'CS': 'cs',
            'CS%': 'cs_percent',
            'W': 'w',
            'D': 'd',
            'L': 'l'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'mp', 'starts', 'min', 'ninety_s', 'ga', 'ga_per_90', 'sota', 'saves', 'save_percent', 
                'w', 'd', 'l', 'cs', 'cs_percent']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'mp': 'int',
            'starts': 'int',
            'min': 'int',
            'ninety_s': 'float',
            'ga': 'int',
            'ga_per_90': 'float',
            'sota': 'int',
            'saves': 'int',
            'save_percent': 'float',
            'w': 'int',
            'd': 'int',
            'l': 'int',
            'cs': 'int',
            'cs_percent': 'float'
        })

    def _transform_team_miscellaneous_stats(self, df):
        """Transform the Team Miscellaneous Stats data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'CrdY': 'crd_y',
            'CrdR': 'crd_r',
            '2CrdY': 'two_crd_y',
            'Fls': 'fls',
            'Fld': 'fld',
            'Off': 'off',
            'Crs': 'crs',
            'Int': 'interceptions',
            'TklW': 'tklw',
            'PKwon': 'pkwon',
            'PKcon': 'pkcon',
            'OG': 'og',
            'Recov': 'recov',
            'Won': 'won',
            'Lost': 'lost',
            'Won%': 'won_percent'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'crd_y', 'crd_r', 'two_crd_y', 'fls', 'fld', 'off', 'crs', 
                'interceptions', 'tklw', 'pkwon', 'pkcon', 'og', 'recov', 'won', 'lost', 'won_percent']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'crd_y': 'int',
            'crd_r': 'int',
            'two_crd_y': 'int',
            'fls': 'int',
            'fld': 'int',
            'off': 'int',
            'crs': 'int',
            'interceptions': 'int',
            'tklw': 'int',
            'pkwon': 'int',
            'pkcon': 'int',
            'og': 'int',
            'recov': 'int',
            'won': 'int',
            'lost': 'int',
            'won_percent': 'float'
        })

    def _transform_team_pass_types(self, df):
        """Transform the Team Pass Types data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Att': 'att',
            'Live': 'live',
            'Dead': 'dead',
            'FK': 'fk',
            'TB': 'tb',
            'Sw': 'sw',
            'Crs': 'crs',
            'TI': 'ti',
            'CK': 'ck',
            'In': 'inn',
            'Out': 'outt',
            'Str': 'str',
            'Cmp': 'cmp',
            'Off': 'off',
            'Blocks': 'blocks'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'att', 'live', 'dead', 'fk', 'tb', 'sw', 'crs', 'ti', 'ck', 'inn', 'outt', 
                'str', 'cmp', 'off', 'blocks']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'att': 'int',
            'live': 'int',
            'dead': 'int',
            'fk': 'int',
            'tb': 'int',
            'sw': 'int',
            'crs': 'int',
            'ti': 'int',
            'ck': 'int',
            'inn': 'int',
            'outt': 'int',
            'str': 'int',
            'cmp': 'int',
            'off': 'int',
            'blocks': 'int'
        })

    def _transform_team_passing(self, df):
        """Transform the Team Passing data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Cmp_total': 'cmp_total',
            'Att_total': 'att_total',
            'Cmp%_total': 'cmp_percent_total',
            'TotDist_total': 'tot_dist_total',
            'PrgDist_total': 'prg_dist_total',
            'Cmp_short': 'cmp_short',
            'Att_short': 'att_short',
            'Cmp%_short': 'cmp_percent_short',
            'Cmp_medium': 'cmp_medium',
            'Att_medium': 'att_medium',
            'Cmp%_medium': 'cmp_percent_medium',
            'Cmp_long': 'cmp_long',
            'Att_long': 'att_long',
            'Cmp%_long': 'cmp_percent_long',
            'Ast': 'ast',
            'xAG': 'xag',
            'xA': 'xa',
            'KP': 'kp',
            '1/3': 'one_third',
            'CrsPA': 'crspa',
            'PrgP': 'prgp'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'cmp_total', 'att_total', 'cmp_percent_total', 'tot_dist_total', 
                'prg_dist_total', 'cmp_short', 'att_short', 'cmp_percent_short', 'cmp_medium', 'att_medium', 
                'cmp_percent_medium', 'cmp_long', 'att_long', 'cmp_percent_long', 'ast', 'kp', 'one_third', 'crspa', 
                'prgp']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'cmp_total': 'int',
            'att_total': 'int',
            'cmp_percent_total': 'float',
            'tot_dist_total': 'float',
            'prg_dist_total': 'float',
            'cmp_short': 'int',
            'att_short': 'int',
            'cmp_percent_short': 'float',
            'cmp_medium': 'int',
            'att_medium': 'int',
            'cmp_percent_medium': 'float',
            'cmp_long': 'int',
            'att_long': 'int',
            'cmp_percent_long': 'float',
            'ast': 'int',
            'kp': 'int',
            'one_third': 'int',
            'crspa': 'int',
            'prgp': 'int'
        })

    def _transform_team_playing_time(self, df):
        """Transform the Team Playing Time data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            'Age': 'age',
            'MP': 'mp',
            'Min': 'min',
            'Mn/MP': 'mn_per_mp',
            'Min%': 'min_percent',
            '90s': 'ninety_s',
            'Starts': 'starts',
            'Mn/Start': 'mn_per_start',
            'Compl': 'compl',
            'Subs': 'subs',
            'Mn/Sub': 'mn_per_sub',
            'unSub': 'unsub',
            'PPM': 'ppm',
            'onG': 'on_g',
            'onGA': 'on_ga',
            '+/-': 'plus_minus',
            '+/-90': 'plus_minus_per_90',
            'onxG': 'onxg',
            'onxGA': 'onxga',
            'xG+/-': 'xg_plus_minus',
            'xG+/-90': 'xg_plus_minus_per_90'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'age', 'mp', 'min', 'mn_per_mp', 'min_percent', 'ninety_s', 'starts', 
                'mn_per_start', 'compl', 'subs', 'mn_per_sub', 'unsub', 'ppm', 'on_g', 'on_ga', 'plus_minus', 
                'plus_minus_per_90', 'onxg', 'onxga', 'xg_plus_minus', 'xg_plus_minus_per_90']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'age': 'float',
            'mp': 'int',
            'min': 'int',
            'mn_per_mp': 'float',
            'min_percent': 'float',
            'ninety_s': 'float',
            'starts': 'int',
            'mn_per_start': 'float',
            'compl': 'int',
            'subs': 'int',
            'mn_per_sub': 'float',
            'unsub': 'int',
            'ppm': 'float',
            'on_g': 'int',
            'on_ga': 'int',
            'plus_minus': 'int',
            'plus_minus_per_90': 'float',
            'onxg': 'float',
            'onxga': 'float',
            'xg_plus_minus': 'float',
            'xg_plus_minus_per_90': 'float'
        })

    def _transform_team_possession(self, df):
        """Transform the Team Possession data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Touches': 'touches',
            'Def Pen': 'def_pen',
            'Def 3rd': 'def_3rd',
            'Mid 3rd': 'mid_3rd',
            'Att 3rd': 'att_3rd',
            'Att Pen': 'att_pen',
            'Live': 'live',
            'Att': 'att',
            'Succ': 'succ',
            'Succ%': 'succ_percent',
            'Tkld': 'tkld',
            'Tkld%': 'tkld_percent',
            'Carries': 'carries',
            'TotDist': 'tot_dist',
            'PrgDist': 'prg_dist',
            'PrgC': 'prgc',
            '1/3': 'one_third',
            'CPA': 'cpa',
            'Mis': 'mis',
            'Dis': 'dis',
            'Rec': 'rec',
            'PrgR': 'prgr'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'touches', 'def_pen', 'def_3rd', 'mid_3rd', 'att_3rd', 'att_pen', 
                'live', 'att', 'succ', 'succ_percent', 'tkld', 'tkld_percent', 'carries', 'tot_dist', 'prg_dist', 
                'prgc', 'one_third', 'cpa', 'mis', 'dis', 'rec', 'prgr']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'touches': 'int',
            'def_pen': 'int',
            'def_3rd': 'int',
            'mid_3rd': 'int',
            'att_3rd': 'int',
            'att_pen': 'int',
            'live': 'int',
            'att': 'int',
            'succ': 'int',
            'succ_percent': 'float',
            'tkld': 'int',
            'tkld_percent': 'float',
            'carries': 'int',
            'tot_dist': 'float',
            'prg_dist': 'float',
            'prgc': 'int',
            'one_third': 'int',
            'cpa': 'int',
            'mis': 'int',
            'dis': 'int',
            'rec': 'int',
            'prgr': 'int'
        })

    def _transform_team_shooting(self, df):
        """Transform the Team Shooting data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            '90s': 'ninety_s',
            'Gls': 'gls',
            'Sh': 'sh',
            'SoT': 'sot',
            'SoT%': 'sot_percent',
            'Sh/90': 'sh_per_90',
            'SoT/90': 'sot_per_90',
            'G/Sh': 'g_per_sh',
            'G/SoT': 'g_per_sot',
            'Dist': 'dist',
            'FK': 'fk',
            'PK': 'pk',
            'PKatt': 'pkatt',
            'xG': 'xg',
            'npxG': 'npxg',
            'npxG/Sh': 'npxg_per_sh',
            'G-xG': 'g_minus_xg',
            'np:G-xG': 'npg_minus_xg'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'ninety_s', 'gls', 'sh', 'sot', 'sot_percent', 'sh_per_90', 'sot_per_90', 
                'g_per_sh', 'g_per_sot', 'dist', 'fk', 'pk', 'pkatt', 'xg', 'npxg', 'npxg_per_sh', 
                'g_minus_xg', 'npg_minus_xg']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'ninety_s': 'float',
            'gls': 'int',
            'sh': 'int',
            'sot': 'int',
            'sot_percent': 'float',
            'sh_per_90': 'float',
            'sot_per_90': 'float',
            'g_per_sh': 'float',
            'g_per_sot': 'float',
            'dist': 'float',
            'fk': 'int',
            'pk': 'int',
            'pkatt': 'int',
            'xg': 'float',
            'npxg': 'float',
            'npxg_per_sh': 'float',
            'g_minus_xg': 'float',
            'npg_minus_xg': 'float'
        })

    def _transform_team_standard_stats(self, df):
        """Transform the Team Standard Stats data to match the schema."""
        # Drop unnecessary columns: 'Squad', '# Pl'
        df.drop(columns=['Squad', '# Pl'], inplace=True)

        # Add new empty columns 'stat_id' and 'team_id'
        df['stat_id'] = None  # Empty stat_id, to be generated by the database
        df['team_id'] = None  # Empty team_id, to be filled later

        # Rename the columns to match the database table schema
        df.rename(columns={
            'Age': 'age',
            'Poss': 'poss',
            'MP': 'mp',
            'Starts': 'starts',
            'Min': 'min',
            '90s': 'ninety_s',
            'Gls': 'gls',
            'Gls_per_90': 'gls_per_90',
            'Ast': 'ast',
            'Ast_per_90': 'ast_per_90',
            'G+A': 'g_a',
            'G+A_per_90': 'g_a_per_90',
            'G-PK': 'g_pk',
            'G-PK_per_90': 'g_pk_per_90',
            'PK': 'pk',
            'PKatt': 'pkatt',
            'CrdY': 'crd_y',
            'CrdR': 'crd_r',
            'xG': 'xg',
            'xG_per_90': 'xg_per_90',
            'npxG': 'npxg',
            'npxG_per_90': 'npxg_per_90',
            'xAG': 'xag',
            'xAG_per_90': 'xag_per_90',
            'npxG+xAG': 'npxg_xag',
            'npxG+xAG_per_90': 'npxg_xag_per_90'
        }, inplace=True)

        # Return columns in the correct order for database insertion
        return df[['stat_id', 'team_id', 'age', 'poss', 'mp', 'starts', 'min', 'ninety_s', 'gls', 'gls_per_90', 
                'ast', 'ast_per_90', 'g_a', 'g_a_per_90', 'g_pk', 'g_pk_per_90', 'pk', 'pkatt', 'crd_y', 
                'crd_r', 'xg', 'xg_per_90', 'npxg', 'npxg_per_90', 'xag', 'xag_per_90', 'npxg_xag', 
                'npxg_xag_per_90']].astype({
            'stat_id': 'Int64',  # Nullable integer
            'team_id': 'Int64',  # Nullable integer
            'age': 'float',
            'poss': 'float',
            'mp': 'int',
            'starts': 'int',
            'min': 'int',
            'ninety_s': 'float',
            'gls': 'int',
            'gls_per_90': 'float',
            'ast': 'int',
            'ast_per_90': 'float',
            'g_a': 'int',
            'g_a_per_90': 'float',
            'g_pk': 'int',
            'g_pk_per_90': 'float',
            'pk': 'int',
            'pkatt': 'int',
            'crd_y': 'int',
            'crd_r': 'int',
            'xg': 'float',
            'xg_per_90': 'float',
            'npxg': 'float',
            'npxg_per_90': 'float',
            'xag': 'float',
            'xag_per_90': 'float',
            'npxg_xag': 'float',
            'npxg_xag_per_90': 'float'
        })
                

