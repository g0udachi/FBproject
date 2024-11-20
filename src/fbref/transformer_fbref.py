import os
import pandas as pd

class FBRefTransformer:
    def __init__(self, data):
        self.data = data
        self.base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'fbref_data')

    def save_dataframes(self):
        for league, dataframes in self.data.items():
            league_path = os.path.join(self.base_path, league)
            os.makedirs(league_path, exist_ok=True)
            
            for table_name, df in dataframes.items():
                file_name = f"{table_name}.csv"
                file_path = os.path.join(league_path, file_name)
                df.to_csv(file_path, index=False)
                print(f"Saved {file_name} for {league} to {file_path}")

# Example usage
if __name__ == "__main__":
    # This example assumes all_data has been fetched from the scraper
    # Create an instance of FBRefTransformer with the fetched data
    from fbref.scraper_fbref import FBRefScraper

    scraper = FBRefScraper()
    all_data = scraper.scrape_all()

    transformer = FBRefTransformer(data=all_data)
    transformer.save_dataframes()
