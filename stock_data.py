# stock_data.py
import yfinance as yf

def download_stock_data(ticker, start, end):
    """
    Downloads historical stock data for a given ticker symbol.

    Parameters:
        - ticker (str): Ticker symbol for the stock.
        - start (str): Start date in 'YYYY-MM-DD' format.
        - end (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pandas.DataFrame: Historical stock data.
    """
    try:
        stock_data = yf.download(ticker, start, end)
        return stock_data
    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")
        return None
