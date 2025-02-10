import logging
import asyncio
from services.websocket_management import WebSocketSymbol, subscribe_to_futures_price, subscribe_to_spot_price, initialize_websocket

class TriangularArbitrage:
    """
    Class to manage the triangular arbitrage strategy.
    type: str - "spot" or "futures"
    """
    def __init__(self, first_symbol: str, intermediary_symbol: str, last_symbol: str, type: str):
        self.first_symbol = WebSocketSymbol(first_symbol)
        self.intermediary_symbol = WebSocketSymbol(intermediary_symbol)
        self.last_symbol = WebSocketSymbol(last_symbol)
        self.type = type


    async def start(self):
        await asyncio.gather(
            self.websocket_main(),
            self.manage_triangular_abritrage()
        )


    async def websocket_main(self):
        """
        Main function to initialize WebSocket and subscribe to price updates.
        """
        # Initialize WebSocket service
        ws_service = initialize_websocket()

        # Create Spot and Futures WebSocket clients
        spot_ws = ws_service.new_spot_public_ws()
        futures_ws = ws_service.new_futures_public_ws()

        # Run all subscriptions concurrently
        if (self.type == "spot"):
            await asyncio.gather(
                subscribe_to_spot_price(spot_ws, self.first_symbol),
                subscribe_to_spot_price(spot_ws, self.intermediary_symbol),
                subscribe_to_spot_price(spot_ws, self.last_symbol),
            )
        elif (self.type == "futures"):
            await asyncio.gather(
                subscribe_to_futures_price(futures_ws, self.first_symbol),
                subscribe_to_futures_price(futures_ws, self.intermediary_symbol),
                subscribe_to_futures_price(futures_ws, self.last_symbol),
            )
        else:
            logging.error(f"Invalid type provided. Please enter 'spot' or 'futures'. Chosen : {self.type}")


    async def manage_triangular_abritrage(self):
        logging.info(f"Starting triangular arbitrage for {self.first_symbol.symbol}, {self.intermediary_symbol.symbol}, {self.last_symbol.symbol}")

        while not self.verify_price_initialization():
            await asyncio.sleep(3)
            logging.info(f"Waiting for prices to be initialized for {self.first_symbol.symbol}, {self.intermediary_symbol.symbol}, {self.last_symbol.symbol}")

        while True:
            await asyncio.sleep(0.1)
            self.calculate_triangular_arbitrage_for_ask_price()

        logging.critical("wtf, this code should never be reached")



    def calculate_triangular_arbitrage_for_ask_price(self):
        # Calculate the triangular arbitrage price difference
        implied_first_symbol_price = 1 / self.intermediary_symbol.bestAskPrice * self.last_symbol.bestBidPrice
        # if the implied first symbol price (ex : BTCUSDT) is more than the real price, then buying BTC, then ETH from BTC, then selling ETH is a good idea
        real_price = self.first_symbol.bestAskPrice

        logging.info(f"Implied price ({self.intermediary_symbol.symbol}): {implied_first_symbol_price:.6f}")
        self.calculate_triangular_arbitrage_price_difference(implied_first_symbol_price, real_price, "ask")



    def calculate_triangular_arbitrage_price_difference(self, implied_price, real_price, direction: str):
        """
        Calculates the triangular arbitrage price difference for the chosen symbols
        
        Args:
            implied_price (float): The implied price of the triangular arbitrage.
            real_price (float): The real price of the goal symbol.
            direction (str): The direction of the triangular arbitrage ("ask" or "bid").
        """
        price_difference = implied_price - real_price
        logging.info(f"Price difference: {price_difference:.6f}")

        percentage_difference = (price_difference / real_price) * 100
        logging.info(f"Percentage difference: {percentage_difference:.2f}%")


    def verify_price_initialization(self):
        return (self.first_symbol.bestAskPrice != 0 and self.first_symbol.bestBidPrice != 0) and (self.intermediary_symbol.bestAskPrice != 0 and self.intermediary_symbol.bestBidPrice != 0) and (self.last_symbol.bestAskPrice != 0 and self.last_symbol.bestBidPrice != 0)

