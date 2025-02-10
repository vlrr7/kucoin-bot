import logging
from utils.utils import get_current_market_price

class Symbol:
    def __init__(self, symbol, market_api):
        self.symbol = symbol
        self.price = get_current_market_price(market_api, symbol)
        self.log_price()

    def log_price(self):
        logging.info(f"Current price for {self.symbol}: {self.price:.6f}")


def calculate_triangular_abritrage(market_api):
    """
    Calculates the triangular arbitrage price difference for BTC-USDT, ETH-BTC, and ETH-USDT.
    
    Args:
        market_api: The Spot Market API service.
    
    Returns:
        float: The triangular arbitrage price difference.
    """
    # Fetch the current price of the specified trading pair
    BTCUSDT_symbol = Symbol("BTC-USDT", market_api) 
    ETHBTC_symbol = Symbol("ETH-BTC", market_api) 
    ETHUSDT_symbol = Symbol("ETH-USDT", market_api)

    # Calculate the triangular arbitrage price difference
    BTC = BTCUSDT_symbol.price
    implied_ETHUSDT = BTC * ETHBTC_symbol.price
    logging.info(f"ETH from BTC: {implied_ETHUSDT:.6f}")

    calculate_triangular_arbitrage_price_difference(implied_ETHUSDT, ETHUSDT_symbol.price)


def calculate_triangular_arbitrage_price_difference(implied_ETHUSDT, ETHUSDT):
    # if implied_ETHUSDT < ETHUSDT, then buying BTC, then ETH from BTC, then selling ETH is a good idea
    # if implied_ETHUSDT > ETHUSDT, then buying ETH, then BTC from ETH, then selling BTC is a good idea
    price_difference = implied_ETHUSDT - ETHUSDT
    logging.info(f"Price difference: {price_difference:.6f}")

    percentage_difference = (price_difference / ETHUSDT) * 100
    logging.info(f"Percentage difference: {percentage_difference:.2f}%")

