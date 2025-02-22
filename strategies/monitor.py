import asyncio
import logging
from services.websocket_management import initialize_websocket, subscribe_to_spot_price, WebSocketSymbol

async def monitor(spot_market_api):
    # Initialize WebSocket
    ws_service = initialize_websocket()

    # Symbol to monitor (not yet listed)
    new_symbol = "XOXO-USDT"

    # Poll for new listings (example logic)
    while True:
        try:
            # Check if the symbol exists (use the appropriate API endpoint)
            is_listed = check_if_symbol_is_listed(spot_market_api,"XOXO")  # Implement this function using KuCoin's API
            if is_listed:
                logging.info(f"{new_symbol} is now listed! Subscribing to price updates...")
                spot_ws = initialize_websocket().new_spot_public_ws()
                await subscribe_to_spot_price(spot_ws, WebSocketSymbol(new_symbol))
                break
            else:
                logging.debug(f"{new_symbol} not listed yet. Checking again in 0.1 seconds...")
                await asyncio.sleep(0.1)
        except Exception as e:
            logging.error(f"Error checking for new listings: {e}")
            await asyncio.sleep(60)


def check_available_symbols(spot_market_api) -> set:
    """
    Fetches the list of available trading symbols (pairs) from KuCoin.
    Args:
        spot_market_api (MarketAPI): The market API client instance for the spot market.
    Returns:
        set: A set of available trading symbols (e.g., {"BTC-USDT", "ETH-USDT", ...}).
    """
    try:
        # Fetch all available trading symbols
        symbols_resp = spot_market_api.get_all_currencies()
        logging.debug(f"Available symbols fetched successfully: {symbols_resp.data}.")
        available_symbols = {symbol_data.currency for symbol_data in symbols_resp.data}
        logging.info(f"Available symbols fetched successfully: {len(available_symbols)} symbols.")
        return available_symbols
    except Exception as e:
        logging.error(f"Error fetching available symbols: {e}")
        return set()  # Return an empty set in case of an error


def check_if_symbol_is_listed(spot_market_api, symbol: str) -> bool:
    """
    Checks if a symbol is listed on KuCoin's spot market.
    Args:
        spot_market_api (MarketAPI): The market API client instance for the spot market.
        symbol (str): The symbol to check (e.g., "BTC-USDT").
    Returns:
        bool: True if the symbol is listed, False otherwise.
    """
    try:
        # Fetch the symbol information
        symbol_resp = check_available_symbols(spot_market_api)
        return symbol in symbol_resp
    except Exception as e:
        logging.error(f"Error checking if {symbol} is listed: {e}")
        return False
