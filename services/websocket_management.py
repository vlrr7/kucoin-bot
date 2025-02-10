import asyncio
import os
import logging
from services.config import LOG_WEBSOCKET_PRICES
from kucoin_universal_sdk.api.client import DefaultClient
from kucoin_universal_sdk.generate.spot.spot_public.model_ticker_event import TickerEvent
from kucoin_universal_sdk.generate.futures.futures_public.model_ticker_v2_event import TickerV2Event
from kucoin_universal_sdk.generate.spot.spot_public.ws_spot_public import SpotPublicWS
from kucoin_universal_sdk.generate.futures.futures_public.ws_futures_public import FuturesPublicWS
from kucoin_universal_sdk.model.client_option import ClientOptionBuilder
from kucoin_universal_sdk.model.constants import GLOBAL_API_ENDPOINT, GLOBAL_FUTURES_API_ENDPOINT
from kucoin_universal_sdk.model.websocket_option import WebSocketClientOptionBuilder

class WebSocketSymbol:
    def __init__(self, symbol):
        self.symbol = symbol
        self.bestAskPrice = 0
        self.bestBidPrice = 0

        if "-" in self.symbol:
            self.type = "spot"
        else:
            self.type = "futures"
    
    def isOperational(self):
        return self.bestAskPrice != 0 and self.bestBidPrice != 0
    
    def updatePrices(self, data):
        if self.type == "spot":
            self.updatePricesSpot(data)
        else:
            self.updatePricesFutures(data)

    def updatePricesSpot(self, data: TickerEvent):
        self.bestAskPrice = float(data.best_ask)
        self.bestBidPrice = float(data.best_bid)
        if LOG_WEBSOCKET_PRICES: logging.info(f"[SPOT PRICE] {self.symbol}: Best Ask Price={self.bestAskPrice}, Best Bid Price={self.bestBidPrice}")

    def updatePricesFutures(self, data: TickerV2Event):
        self.bestAskPrice = float(data.best_ask_price)
        self.bestBidPrice = float(data.best_bid_price)
        if LOG_WEBSOCKET_PRICES: logging.info(f"[FUTURES PRICE] {self.symbol}: Best Ask Price={self.bestAskPrice}, Best Bid Price={self.bestBidPrice}")


def initialize_websocket():
    """
    Initializes the Kucoin WebSocket client.
    """
    # Retrieve API credentials from environment variables
    key = os.getenv("KUCOINBOT_API_KEY", "")
    secret = os.getenv("KUCOINBOT_API_SECRET", "")
    passphrase = os.getenv("KUCOINBOT_API_PASSPHRASE", "")

    # Set WebSocket options
    ws_client_option = WebSocketClientOptionBuilder().build()

    # Create a client using the specified options
    client_option = (
        ClientOptionBuilder()
        .set_key(key)
        .set_secret(secret)
        .set_passphrase(passphrase)
        .set_websocket_client_option(ws_client_option)
        .set_spot_endpoint(GLOBAL_API_ENDPOINT)
        .set_futures_endpoint(GLOBAL_FUTURES_API_ENDPOINT)
        .build()
    )
    client = DefaultClient(client_option)
    return client.ws_service()

async def subscribe_to_spot_price(spot_ws: SpotPublicWS, symbol: WebSocketSymbol):
    """
    Subscribes to real-time spot price updates for the specified trading pair.
    
    Args:
        spot_ws (SpotPublicWS): The Spot WebSocket client instance.
        symbol (str): The trading pair symbol (e.g., 'BTC-USDT').
    """
    try:
        # Start WebSocket
        spot_ws.start()

        # Define callback function to handle ticker events
        def ticker_event_callback(topic: str, subject: str, data: TickerEvent) -> None:
            symbol.updatePrices(data)
            # logging.info(f"[SPOT PRICE] {symbol}: Best Ask Price={data.best_ask}, Best Bid Price={data.best_bid}")
            # logging.info(f"received ticker event {data.to_json()}")

        # Subscribe to ticker updates
        sub_id = spot_ws.ticker([symbol.symbol], ticker_event_callback)
        logging.info(f"[SPOT] Subscribed to price updates for {symbol} with subscription ID: {sub_id}")

        # Keep the WebSocket connection alive
        await asyncio.Event().wait()  # Keeps the coroutine alive without blocking

    except Exception as e:
        logging.error(f"[SPOT] Error: {e}")
    finally:
        spot_ws.stop()

async def subscribe_to_futures_price(futures_ws: FuturesPublicWS, symbol: WebSocketSymbol):
    """
    Subscribes to real-time futures price updates for the specified trading pair.
    
    Args:
        futures_ws (FuturesPublicWS): The Futures WebSocket client instance.
        symbol (str): The futures contract symbol (e.g., 'XBTUSDTM').
    """
    try:
        # Start WebSocket
        futures_ws.start()

        # Define callback function to handle ticker events
        def ticker_event_v2_callback(topic: str, subject: str, data: TickerV2Event) -> None:
            symbol.updatePrices(data)
            # logging.info(f"received ticker event {data.to_json()}")
            # logging.info(f"[FUTURES PRICE] {symbol}: Best Ask Price={data.best_ask_price}, Best Bid Price={data.best_bid_price}")

        # Subscribe to ticker updates
        sub_id = futures_ws.ticker_v2(symbol.symbol, ticker_event_v2_callback)
        logging.info(f"[FUTURES] Subscribed to price updates for {symbol} with subscription ID: {sub_id}")

        # Keep the WebSocket connection alive
        while True:
            await asyncio.sleep(60)

    except Exception as e:
        logging.error(f"[FUTURES] Error: {e}")
    finally:
        futures_ws.stop()