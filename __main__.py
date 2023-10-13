import requests
import logging
import time
from ticker import Ticker  # Importing the Ticker class from ticker.py
import asyncio
import concurrent.futures

# Initialize logging, setting the log file and the level of logging.
logging.basicConfig(filename='Program Data/program.log', level=logging.INFO)

def get_roles():
    # Read roles from a file and return them as a dictionary.
    with open('Program Data/roles.txt','r') as f:
        roles = {line.split(',')[0]:line.split(',')[1].strip() for line in f}
        return roles

role_ids = get_roles()  # Retrieve role IDs.

def get_tickers():
    # Read tickers from a file, create Ticker objects, and return them as a list.
    with open('Program Data/tickers.txt','r') as f:
        logging.info("Tickers started")
        tickers = [Ticker(line.strip()) for line in f]
        return tickers

def get_hooks():
    # Read webhooks from a file and return them as a dictionary.
    with open('Program Data/hooks.txt','r') as f:
        hooks = {line.split(',')[0]:line.split(',')[1].strip() for line in f}
        return hooks

def process_indicators(ticker, hooks=get_hooks()):
    # Process various stock indicators and send relevant notifications to Discord.
    try:
        roles = ticker.get_roles()
        sector = ticker._sector
        sector_hook = hooks[sector]
        ticker.update_data()  # Update ticker data.
        
        # Retrieve various stock metrics.
        price = ticker.get_price(False)
        yest_price = ticker.get_price(True)
        percent_move = ticker.get_percent_move(1)
        volume = ticker.get_volume()
        ma_200 = ticker.get_moving_avg(200)
        ma_50 = ticker.get_moving_avg(50)
        avg_volume = ticker.get_average_volume()

        # Check various conditions and send appropriate notifications to Discord.
        # Moving average indicators.
        if price > ma_200 and yest_price < ma_200:
            log_content = f"{ticker} crossed above 200 day moving average"
            send_to_discord(log_content, sector_hook, roles)
        elif price < ma_200 and yest_price > ma_200:
            log_content = f"{ticker} crossed below 200 day moving average"
            send_to_discord(log_content, sector_hook, roles)
        if price > ma_50 and yest_price < ma_50:
            log_content = f"{ticker} crossed above 50 day moving average"
            send_to_discord(log_content, sector_hook, roles)
        elif price < ma_50 and yest_price > ma_50:
            log_content = f"{ticker} crossed below 50 day moving average"
            send_to_discord(log_content, sector_hook, roles)
        # Price indicators.
        if percent_move >= 3:
            log_content = f"{ticker} gained {percent_move}% since yesterday"
            send_to_discord(log_content, sector_hook, roles)
        elif percent_move <= -3:
            log_content = f"{ticker} lost {percent_move}% since yesterday"
            send_to_discord(log_content, sector_hook, roles)
        # Volume indicator.
        if volume > (avg_volume * 1.5):
            log_content = f"Today, {ticker}'s volume was {round(((volume/avg_volume)-1)*100,2)}% above average"
            send_to_discord(log_content, sector_hook, roles)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        pass

def send_to_discord(log_content, hook_url, roles):
    # Send messages to Discord using webhooks.
    mentions = ""
    for role in roles:
        mentions += f"<@&{role_ids[role]}>"
    
    data = {
        'content': f"{mentions}: {log_content}"
    }
    requests.post(hook_url, json=data)
    logging.info(f"Sent to Discord: {log_content}")

async def process_all_tickers(tickers):
    # Asynchronously process all tickers using a ThreadPoolExecutor.
    logging.info(f"Starting processing of {len(tickers)} tickers")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                process_indicators, 
                ticker
            )
            for ticker in tickers
        ]
        logging.info(f"All tasks submitted to the executor")
        for response in await asyncio.gather(*futures):
            pass  # process response if needed
    logging.info("Finished processing all tickers")

def main():
    # Main function to execute the script.
    start_time = time.time()
    logging.info("Program started")
    tickers = get_tickers()  # Retrieve all tickers.
    asyncio.run(process_all_tickers(tickers))  # Process all tickers.
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Program ended successfully. Total runtime: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()  # Run the main function when the script is executed.
