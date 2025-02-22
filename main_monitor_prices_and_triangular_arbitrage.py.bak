import logging
import asyncio
from services.config import initialize_kucoin_client, get_market_api
from services.websocket_management import initialize_websocket, subscribe_to_spot_price, subscribe_to_futures_price
from services.announcements import get_new_listings
from utils.utils import get_current_market_price, get_current_market_price_as_log
from strategies.triangular_arbitrage import TriangularArbitrage
from strategies.monitor import monitor, check_available_symbols

# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

if __name__ == "__main__":
    try:
        # Initialize the Kucoin client
        client = initialize_kucoin_client()
        market_api = get_market_api(client)


        # check_available_symbols(market_api)
        # logging.info(get_new_listings(market_api))
        asyncio.run(monitor(spot_market_api=market_api))


    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Error: {e}")



def start_arbitrage():
    ETHBTC_triangular_arbitrage = TriangularArbitrage("BTC-USDT", "ETH-BTC", "ETH-USDT", "spot")
    # USDCUSDT_triangular_arbitrage = TriangularArbitrage("USDCUSDTM", "XBTUSDCM", "XBTUSDTM", "futures")
    asyncio.run(ETHBTC_triangular_arbitrage.start())
    # asyncio.run(USDCUSDT_triangular_arbitrage.start())