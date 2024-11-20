import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import logging
from config.fbref_config import FBREF_PLAYERS_STATS_URLS  # Import the URLs from the config file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FBRefPlayerScraper:
    def __init__(self, save_path, delay=4):
        self.save_path = save_path
        self.delay = delay

        if not os.path.exists(save_path):
            os.makedirs(save_path)

    def fetch_page(self, url):
        """Fetch HTML content from a URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching page {url}: {e}")
            return ""

    def parse_table(self, soup, table_wrapper_id, table_id):
        """Parse a table from the BeautifulSoup object, including commented tables."""
        # Find the specific wrapper by its ID
        wrapper = soup.find('div', {'id': table_wrapper_id})
        if wrapper:
            # The table might be within a commented section, so let's handle that
            comment = wrapper.find(string=lambda text: isinstance(text, str) and table_id in text)
            if comment:
                # Remove comment tags and parse the table
                comment_soup = BeautifulSoup(comment, 'html.parser')
                table = comment_soup.find('table', {'id': table_id})
            else:
                # If not found in comments, find directly in the wrapper
                table = wrapper.find('table', {'id': table_id})

            if table:
                table_html = str(table)
                return pd.read_html(StringIO(table_html))[0]  # Use StringIO to parse table HTML to DataFrame
            else:
                logging.warning(f"Table with ID {table_id} not found inside wrapper {table_wrapper_id}.")
                return pd.DataFrame()  # Return an empty DataFrame if the table is not found
        else:
            logging.warning(f"Wrapper with ID {table_wrapper_id} not found.")
            return pd.DataFrame()

    def scrape_player_data(self, league_name, url, table_wrapper_id, table_id):
        """Scrape and save player data for a specific table and league."""
        logging.info(f"Scraping {table_id} for {league_name} from {url}...")
        html = self.fetch_page(url)
        if not html:
            return

        soup = BeautifulSoup(html, 'html.parser')
        df = self.parse_table(soup, table_wrapper_id, table_id)

        if not df.empty:
            # Create a folder for the league if it doesn't exist
            league_folder_path = os.path.join(self.save_path, league_name)
            os.makedirs(league_folder_path, exist_ok=True)
            
            # Create file name from table name and league name
            table_name = table_id.replace('stats_', '').replace('_', ' ').title()
            filename = f"{table_name.replace(' ', '_')}.csv"
            file_path = os.path.join(league_folder_path, filename)
            df.to_csv(file_path, index=False)
            logging.info(f"Data saved to {file_path}")
        else:
            logging.warning(f"No data found for {table_id} in {league_name}.")

    def scrape_league(self, league_name, urls):
        """Scrape all player data tables for a specific league."""
        logging.info(f"Scraping league: {league_name}")

        # Table ID map based on the structure provided
        table_wrapper_id_map = {
            'stats': 'all_stats_standard',
            'keepers': 'all_stats_keeper',
            'keepersadv': 'all_stats_keeper_adv',
            'shooting': 'all_stats_shooting',
            'passing': 'all_stats_passing',
            'passing_types': 'all_stats_passing_types',
            'gca': 'all_stats_gca',
            'defense': 'all_stats_defense',
            'possession': 'all_stats_possession',
            'playingtime': 'all_stats_playing_time',
            'misc': 'all_stats_misc'
        }

        table_id_map = {
            'stats': 'stats_standard',
            'keepers': 'stats_keeper',
            'keepersadv': 'stats_keeper_adv',
            'shooting': 'stats_shooting',
            'passing': 'stats_passing',
            'passing_types': 'stats_passing_types',
            'gca': 'stats_gca',
            'defense': 'stats_defense',
            'possession': 'stats_possession',
            'playingtime': 'stats_playing_time',
            'misc': 'stats_misc'
        }

        # Iterate through each URL and determine which table to scrape
        for url in urls:
            # Extract the key part of the URL to match with the table ID map
            key_part = url.split('/')[-2]
            table_wrapper_id = table_wrapper_id_map.get(key_part)
            table_id = table_id_map.get(key_part)

            if table_wrapper_id and table_id:
                # Scrape the data table for this category
                self.scrape_player_data(league_name, url, table_wrapper_id, table_id)
                time.sleep(self.delay)
            else:
                logging.warning(f"URL {url} does not match any known table ID patterns.")

    def scrape_all_leagues(self):
        """Scrape all leagues provided in FBREF_PLAYERS_STATS_URLS."""
        for league_name, urls in FBREF_PLAYERS_STATS_URLS.items():
            self.scrape_league(league_name, urls)

# Example usage
if __name__ == "__main__":
    # Define save path
    save_path = r"C:\Users\asus\Desktop\Football_project\data\fbref_players_data"

    scraper = FBRefPlayerScraper(save_path)
    scraper.scrape_all_leagues()
