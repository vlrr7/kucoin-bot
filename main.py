import logging
from config import initialize_kucoin_client, get_market_api
from utils import get_current_market_price, get_current_market_price_as_log

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    try:
        # Initialize the Kucoin client
        client = initialize_kucoin_client()
        market_api = get_market_api(client)

        # Specify the trading pair to test
        symbol = "SOL-USDT"

        # Fetch and log the current price
        logging.info(get_current_market_price_as_log(market_api, symbol))

    except Exception as e:
        logging.error(f"Error: {e}")