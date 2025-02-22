import logging
from services.config import initialize_kucoin_client, get_market_api
from services.kucoin_services import fetch_all_klines, fetch_klines
from datetime import datetime, timezone
from utils.statistics import save_data_to_csv
import asyncio

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

        # data = fetch_klines(market_api, "BTC-USDT", "1hour", datetime(2025, 2, 10, 15, 0, 0, tzinfo=timezone.utc), datetime(2025, 2, 22, 18, 0, 0, tzinfo=timezone.utc))
        data = asyncio.run(fetch_all_klines(market_api, "BTC-USDT", "1hour", datetime(2018, 1, 1, 0, 0, 0, tzinfo=timezone.utc), datetime(2025, 2, 22, 18, 0, 0, tzinfo=timezone.utc)))

        save_data_to_csv(data, "BTC-USDT.csv")

    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    except Exception as e:
        logging.error(f"Error: {e}")