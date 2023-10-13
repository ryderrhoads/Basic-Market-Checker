## Basic-Market-Checker

The "Basic-Market-Checker" repository contains Python scripts designed to check various stock market indicators and send notifications via Discord. Here's a detailed overview:

### Main Features:
1. **Stock Market Monitoring**: The script monitors stock prices, trading volumes, and other relevant indicators.
2. **Discord Notifications**: It sends automated notifications to Discord through webhooks when certain stock market conditions are met.
3. **Data Handling**: The script reads stock tickers and Discord webhook URLs from text files, processes this data, and logs information within the application.

### Key Python Files:
1. **[ticker.py](https://github.com/ryderrhoads/Basic-Market-Checker/blob/main/ticker.py)**: 
   - Defines a `Ticker` class that handles operations related to a stock ticker.
   - Fetches stock data using the `yfinance` library.
   - Calculates various stock indicators such as moving averages, price changes, and trading volumes.
   - Handles errors and logs them appropriately.

2. **[__main__.py](https://github.com/ryderrhoads/Basic-Market-Checker/blob/main/__main__.py)**:
   - Initializes logging and reads data from text files.
   - Defines functions to process stock indicators and send notifications to Discord.
   - Uses asynchronous processing to handle multiple tickers.
   - Logs the start and end of the script execution along with runtime.

### How to Use:
1. **Setup**:
   - Ensure you have the required Python libraries installed (`yfinance`, `requests`, etc.).
   - Configure Discord webhooks and place them in the `Program Data/hooks.txt` file.
   - List the stock tickers you want to monitor in the `Program Data/tickers.txt` file.

2. **Running the Script**:
   - Execute the script. It will start monitoring the listed stock tickers and send notifications to Discord when certain conditions are met (e.g., significant price changes, volume increases, etc.).

3. **Logging**:
   - The script maintains a log file (`Program Data/program.log`) where it records various events and errors.

### Repository Structure:
- `.github/workflows/`: Contains GitHub Actions workflows.
- `Program Data/`: Contains text files with data like Discord webhooks, stock tickers, and roles.
- `__main__.py` and `ticker.py`: Main Python scripts.

### Note:
- This script is intended to be run as a standalone application. Ensure you comply with market data provider terms and Discord's terms of service.

---

You are currently on the free plan which has a limited number of requests. To increase your quota, you can check available plans by following this [link](https://c7d59216ee8ec59bda5e51ffc17a994d.auth.portal-pluginlab.ai/pricing).

For more information, you can visit the following resources:
- [Website](blank)
- [Documentation](blank)
- [GitHub](blank)
- [X / Twitter](blank)
