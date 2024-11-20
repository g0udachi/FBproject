# src/main.py

from config.fbref_config import LEAGUE_PATHS, PLAYERS_PATHS, SAVE_FOLDER
from fbref.scraper_fbref import FBRefScraper
from fbref.transformer_fbref import FBRefTransformer
from fbref.fbref_players_scraper import FBRefPlayerScraper  # Import the player scraper class
from fbref.cleaning_data import DataCleaner  # Import the data cleaner class
from fbref.cleaning_players_data import PlayerDataCleaner  # Import the player data cleaner class
from fbref.regroup import RegroupData
from database.db_insertion import DataInserter
from fbref.final_data_transformation import FinalDataTransformation


def main():
    #Scraping league-level data
    scraper = FBRefScraper()
    all_data = scraper.scrape_all()
    
    # Print the names of the DataFrames to verify they were created
    for league, dataframes in all_data.items():
         print(f"Data for league: {league}")
         for table_name in dataframes.keys():
             print(f" - {table_name}")
    
    # Transform and save the league data
    transformer = FBRefTransformer(data=all_data)
    transformer.save_dataframes()  # Save the league-level data
    
    # Define the save path for the player data
    save_path = r"C:\Users\asus\Desktop\Football_project\data\fbref_players_data"
    
    # Scraping player-level data
    player_scraper = FBRefPlayerScraper(save_path=save_path)  # Provide the save path
    
    # Call the correct method to scrape all leagues
    player_scraper.scrape_all_leagues()  # This will scrape and save all player tables as CSVs
    
    # Define paths for data cleaning
    data_folder = r"C:\Users\asus\Desktop\Football_project\data\fbref_data"
    cleaned_data_folder = r"C:\Users\asus\Desktop\Football_project\cleaned_data"
    
    # Clean the data
    cleaner = DataCleaner(data_folder=data_folder, cleaned_data_folder=cleaned_data_folder)
    cleaner.clean_squad_standard_stats()  # Execute the cleaning process for Squad Standard Stats
    cleaner.clean_squad_goalkeeping_stats()  # Execute the cleaning process for Squad Goalkeeping Stats
    cleaner.clean_squad_advanced_goalkeeping_stats()  # Execute the cleaning process for Squad Advanced Goalkeeping Stats
    cleaner.clean_squad_shooting_stats()  # Execute the cleaning process for Squad Shooting Stats
    cleaner.clean_squad_passing_stats()  # Execute the cleaning process for Squad Passing Stats
    cleaner.clean_squad_pass_types_stats()  # Execute the cleaning process for Squad Pass Types Stats
    cleaner.clean_squad_goal_and_shot_creation_stats()  # Execute the cleaning process for Squad Goal and Shot Creation Stats
    cleaner.clean_squad_defensive_actions_stats()  # Execute the cleaning process for Squad Defensive Actions Stats
    cleaner.clean_squad_possession_stats()  # Execute the cleaning process for Squad Possession Stats
    cleaner.clean_squad_playing_time_stats()  # Execute the cleaning process for Squad Playing Time Stats
    cleaner.clean_squad_miscellaneous_stats()  # Execute the cleaning process for Squad Miscellaneous Stats

    # Define paths for player data cleaning
    player_data_folder = r"C:\Users\asus\Desktop\Football_project\data\fbref_players_data"
    
    # Clean the player data
    player_cleaner = PlayerDataCleaner(players_data_folder=player_data_folder, cleaned_data_folder=cleaned_data_folder)
    player_cleaner.clean_standard_stats()  # Execute the cleaning process for Standard Player Stats
    player_cleaner.clean_keeper_stats()
    player_cleaner.clean_keeper_adv_stats()
    player_cleaner.clean_shooting_stats()
    player_cleaner.clean_passing_stats()
    player_cleaner.clean_passing_types_stats()
    player_cleaner.clean_gca_stats()
    player_cleaner.clean_defense_stats()
    player_cleaner.clean_possession_stats()
    player_cleaner.clean_playing_time_stats()
    player_cleaner.clean_misc_stats()
    
    # Initialize regroup data class
    # regroup_data = RegroupData(SAVE_FOLDER)

    # Create league table
    # regroup_data.create_league_table()

    # Create team table
    # regroup_data.create_team_table(LEAGUE_PATHS)

    # Create player table
    # regroup_data.create_player_table(PLAYERS_PATHS)
    
    # Create an instance of the FinalDataTransformation class
    #transformer = FinalDataTransformation()

    # Call the transform_and_save method to perform the transformations
    #transformer.transform_and_save()
    
    
    
    
    
    

    # print("Data transformation and saving completed successfully.")
    
    #data_inserter = DataInserter()

    # Essential files to insert first
    #essential_files = ['leagues.csv', 'teams.csv', 'players.csv']
    
    # Call the bulk_insert method to insert the essential files and the rest
    #data_inserter.bulk_insert(essential_files, None)

if __name__ == "__main__":
    main()
