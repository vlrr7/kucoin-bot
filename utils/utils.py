from kucoin_universal_sdk.generate.spot.market.model_get_ticker_req import GetTickerReqBuilder
from datetime import datetime

# Specific Log
def log_to_file(message: str, file_name: str) -> None:
    """
    Logs a single message into the specified file.

    Args:
        message (str): The message to log.
        file_name (str): The name of the file to log the message into.
    """
    try:
        # Open the file in append mode and write the message with a timestamp
        with open(file_name, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            file.write(f"{timestamp} - {message}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def get_current_market_price(market_api, symbol):
    """
    Fetches the current price of a specified trading pair.
    
    Args:
        market_api: The Spot Market API service.
        symbol (str): The trading pair symbol (e.g., 'BTC-USDT', 'DOGE-USDT').
    
    Returns:
        float: The current price of the specified trading pair.
    """
    try:
        # Build the request to fetch the ticker for the specified symbol
        ticker_req = GetTickerReqBuilder().set_symbol(symbol).build()
        ticker_resp = market_api.get_ticker(ticker_req)
        
        # Extract and return the price as a float
        current_price = float(ticker_resp.price)
        return current_price
    except Exception as e:
        raise RuntimeError(f"Failed to fetch price for {symbol}: {e}")
    

def get_current_market_price_as_log(market_api, symbol):
    """
    The same as the get_current_market_price, expect it returns a string to log.
    """
    return f"Current price for {symbol}: {get_current_market_price(market_api, symbol):.6f}"