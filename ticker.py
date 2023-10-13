import yfinance as yf
import os
import datetime
import pandas as pd
import logging  
from os import path

# Setup logging to store logs in 'Program Data/program.log'.
logging.basicConfig(filename='Program Data/program.log', level=logging.INFO)

class Ticker:
    def __init__(self, ticker: str) -> None:
        # Initialize with a ticker symbol, convert to uppercase, and check/create data file.
        self._ticker = ticker.upper() 
        file_path = f"Ticker Data/{self._ticker}.csv"
        if not os.path.exists(file_path):
            self.get_data()  # Fetch data if not already present.
        self._df = self.df()  # Load data into a DataFrame.
        self._marketcap = self.get_market_cap()  # Retrieve market capitalization.
        self._sector = self.get_sector()  # Retrieve the sector of the stock.
        # Dictionary for sector categorization.
        self._sector_dict = {'Utilities': "Utilities", 'Basic Materials': "Materials", 'Healthcare': "Healthcare", 
                             'Technology': "Technology", 'Financial Services': "Financials", 
                             'Consumer Defensive': "Consumer", 'Consumer Cyclical': "Consumer", 
                             'Real Estate': "Real Estate", 'Energy': "Energy", 'Communication Services': "Communications", 
                             'Industrials': "Industrials"}

    def __str__(self) -> str:
        # String representation of the instance, returning the ticker symbol.
        return self._ticker
    
    def df(self) -> pd.DataFrame:
        # Load the CSV file into a DataFrame and return it, log an error if file not found.
        try:
            df = pd.read_csv(f'Ticker Data/{self._ticker}.csv')
            return df   
        except FileNotFoundError:
            logging.error(f"Error: File {self._ticker}.csv not found.")
            return None
    
    def get_roles(self):
        # Determine and return the market cap category and sector of the stock.
        roles = []
        if self._marketcap > 200000000000:
            roles.append("Mega Cap")
        elif self._marketcap > 10000000000:
            roles.append("Large Cap")
        elif self._marketcap > 2000000000:
            roles.append("Mid Cap")
        elif self._marketcap > 300000000:
            roles.append("Small Cap")
        
        roles.append(self._sector_dict[self._sector])
        
        return roles

    def get_market_cap(self):
        # Fetch and return the market capitalization, log an error if not found.
        try:
            return yf.Ticker(self._ticker).info['marketCap']
        except KeyError:
            logging.error(f"Error: Market cap not found for {self._ticker}")
            return -1

    def get_volume(self):
        # Retrieve and return the current day's trading volume.
        csv_path = f'Ticker Data/{self._ticker}.csv'
        df = pd.read_csv(csv_path)
        return yf.Ticker(self._ticker).info['volume']

    def get_sector(self):
        # Retrieve the sector, with hardcoded fallbacks for specific tickers, log an error if not found.
        try:
            return yf.Ticker(self._ticker).info['sector']
        except KeyError:
            logging.error(f"Error: Sector not found for {self._ticker}")
            if self._ticker == "L":
                return "Consumer Cyclical"
            elif self._ticker == "BF.B":
                return "Consumer Defensive"
            elif self._ticker == "CAT":
                return "Industrials"
            else:
                return "Unknown"

    def get_price(self, isYesterday: bool):
        # Get the current or previous day's closing price based on the 'isYesterday' flag.
        csv_path = f'Ticker Data/{self._ticker}.csv'
        df = pd.read_csv(csv_path)
        if isYesterday:
            return df.iloc[-1]['Adj Close']
        return yf.Ticker(self._ticker).info['currentPrice']

    def get_moving_avg(self, days: int):
        # Calculate and return the moving average over a specified number of days, log errors if issues occur.
        if self._df is not None:
            try:
                return self._df['Adj Close'].tail(days).mean()
            except KeyError:
                logging.error("Error: Column 'Adj Close' not found in the DataFrame.")
                return None
        else:
            logging.error("Error: DataFrame not available.")
            return None

    def get_average_volume(self):
        # Calculate and return the average trading volume over the last 90 days, log errors if issues occur.
        if self._df is not None:
            try:
                return self._df['Volume'].tail(90).mean()
            except KeyError:
                logging.error("Error: Column 'Volume' not found in the DataFrame.")
                return None
        else:
            logging.error("Error: DataFrame not available.")
            return None

    def get_data(self):
        # Fetch historical data, create necessary directories, and save data as a CSV file.
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.now() - datetime.timedelta(weeks=41)).strftime('%Y-%m-%d')
        data = yf.download(self._ticker, start=start_date, end=end_date)
        
        if not os.path.exists('Ticker Data'):
            os.makedirs('Ticker Data')  # Create directory if it doesn't exist.

        csv_file_path = os.path.join('Ticker Data', f'{self._ticker}.csv')
        data.to_csv(csv_file_path)  # Save data to CSV.
        logging.info(f"Data for {self._ticker} fetched successfully")

    def get_percent_move(self, days: int):
        # Calculate and return the percentage price change over a specified number of days.
        return round((self.get_price(isYesterday=False) / (self._df.iloc[-days]['Adj Close']) - 1) * 100, 2)

    def update_data(self):
        # Update the CSV file with new data, handle errors, and avoid duplicate entries.
        csv_file_path = os.path.join('Ticker Data', f'{self._ticker}.csv')
        if (not os.path.exists('Ticker Data')) or (not os.path.exists(csv_file_path)):
            self.get_data()  # Fetch data if not present.

        df = pd.read_csv(csv_file_path, parse_dates=['Date'])
        last_date_in_df = df['Date'].max()
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        week_ago = (datetime.datetime.now() - datetime.timedelta(weeks=1)).strftime('%Y-%m-%d')
        today_date_pd = pd.to_datetime(today_date)

        if today_date_pd == pd.to_datetime(last_date_in_df):
            df = df[df['Date'] != today_date_pd]

        new_data = yf.download(self._ticker, start=week_ago, end=today_date)
        updated_data = pd.concat([df, new_data.reset_index()], ignore_index=True)
        updated_data = updated_data.drop_duplicates(subset=['Date'])
       
