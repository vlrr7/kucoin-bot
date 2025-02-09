import logging
import asyncio
from services.config import initialize_kucoin_client, get_market_api
from services.websocket_management import initialize_websocket, subscribe_to_spot_price, subscribe_to_futures_price
from utils.utils import get_current_market_price, get_current_market_price_as_log
from strategies.triangular_arbitrage import calculate_triangular_abritrage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

async def websocket_main():
    """
    Main function to initialize WebSocket and subscribe to price updates.
    """
    # Initialize WebSocket service
    ws_service = initialize_websocket()

    # Create Spot and Futures WebSocket clients
    spot_ws = ws_service.new_spot_public_ws()
    futures_ws = ws_service.new_futures_public_ws()

    # Run both subscriptions concurrently
    await asyncio.gather(
        subscribe_to_spot_price(spot_ws, "SOL-USDT"),
        # subscribe_to_futures_price(futures_ws, "SOLUSDTM"),
    )


if __name__ == "__main__":
    try:
        # Initialize the Kucoin client
        client = initialize_kucoin_client()
        market_api = get_market_api(client)

        calculate_triangular_abritrage(market_api)

        asyncio.run(websocket_main())

    except Exception as e:
        logging.error(f"Error: {e}")