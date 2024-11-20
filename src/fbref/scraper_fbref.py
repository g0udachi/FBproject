import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from config.fbref_config import FBREF_URLS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FBRefScraper:
    def __init__(self, delay=4):
        self.delay = delay
        self.dataframes = {}  # Dictionary to store DataFrames

    def fetch_page(self, url):
        """Fetch HTML content from a URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching page {url}: {e}")
            return ""

    def parse_table(self, soup, table_id):
        """Parse a table from the BeautifulSoup object."""
        table = soup.find('table', {'id': table_id})
        if table:
            table_html = str(table)
            return pd.read_html(StringIO(table_html))[0]  # Use StringIO
        else:
            logging.warning(f"Table with ID {table_id} not found.")
            return pd.DataFrame()  # Return an empty DataFrame if the table is not found

    def scrape_league(self, league_name, url):
        """Scrape tables for a specific league and store them in DataFrames."""
        logging.info(f"Scraping {league_name} from {url}...")
        html = self.fetch_page(url)
        if not html:
            return {}  # Return empty if the page couldn't be fetched

        soup = BeautifulSoup(html, 'html.parser')

        tables = {
            "Squad_Standard_Stats": "stats_squads_standard_for",
            "Squad_Goalkeeping": "stats_squads_keeper_for",
            "Squad_Advanced_Goalkeeping": "stats_squads_keeper_adv_for",
            "Squad_Shooting": "stats_squads_shooting_for",
            "Squad_Passing": "stats_squads_passing_for",
            "Squad_Pass_Types": "stats_squads_passing_types_for",
            "Squad_Goal_and_Shot_Creation": "stats_squads_gca_for",
            "Squad_Defensive_Actions": "stats_squads_defense_for",
            "Squad_Possession": "stats_squads_possession_for",
            "Squad_Playing_Time": "stats_squads_playing_time_for",
            "Squad_Miscellaneous_Stats": "stats_squads_misc_for"
        }

        # Store DataFrames in class attribute
        league_dataframes = {}
        for name, table_id in tables.items():
            df = self.parse_table(soup, table_id)
            if not df.empty:
                league_dataframes[f"{league_name}_{name}"] = df

        self.dataframes[league_name] = league_dataframes
        return league_dataframes

    def scrape_all(self):
        """Scrape data from all leagues."""
        all_data = {}
        for league_name, url in FBREF_URLS.items():
            league_dataframes = self.scrape_league(league_name, url)
            all_data[league_name] = league_dataframes
            time.sleep(self.delay)  # Delay between requests
        return all_data

# Example usage
if __name__ == "__main__":
    scraper = FBRefScraper()
    all_data = scraper.scrape_all()
    # Now, scraper.dataframes contains all the DataFrames and can be used in the transformer file.
