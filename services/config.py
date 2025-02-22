import logging
import os
from kucoin_universal_sdk.api.client import DefaultClient
from kucoin_universal_sdk.model.client_option import ClientOptionBuilder
from kucoin_universal_sdk.model.constants import GLOBAL_API_ENDPOINT
from kucoin_universal_sdk.model.transport_option import TransportOptionBuilder
from utils.utils import log_to_file

LOG_WEBSOCKET_PRICES = True
LOG_IN_FILE = True
LOG_FILE_NAME = "app.log"
LOGGER_LEVEL = logging.INFO

# Formatter for the console (colors)
class ColorFormatter(logging.Formatter):
    # Define colors for different log levels
    COLORS = {
        "DEBUG": "\033[90m",  # Blue
        "INFO": "\033[92m",   # Green
        "WARNING": "\033[93m",# Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[91m\033[1m"  # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        color = self.COLORS.get(levelname, self.RESET)
        return f"{color}{message}{self.RESET}"

# Configure logging
logger = logging.getLogger()
logger.setLevel(LOGGER_LEVEL)

if LOG_IN_FILE:
    # Formatter for the file (no ANSI escape sequences)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    default_file_handler = logging.FileHandler(LOG_FILE_NAME)  # For file output
    default_file_handler.setFormatter(file_formatter)
    logger.addHandler(default_file_handler)

    # Add space between sessions in the log file
    log_to_file("\n", LOG_FILE_NAME)


handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

# Test logging
# logging.debug("This is a debug message.")
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")

# KuCoin Client
def initialize_kucoin_client():
    """
    Initializes and returns the Kucoin client with configured options.
    
    Returns:
        DefaultClient: The initialized Kucoin client instance.
    """
    # Retrieve API credentials from environment variables
    key = os.getenv("KUCOINBOT_API_KEY", "")
    secret = os.getenv("KUCOINBOT_API_SECRET", "")
    passphrase = os.getenv("KUCOINBOT_API_PASSPHRASE", "")

    # Configure transport options
    http_transport_option = (
        TransportOptionBuilder()
        .set_keep_alive(True)
        .set_max_pool_size(10)
        .set_max_connection_per_pool(10)
        .build()
    )

    # Configure client options
    client_option = (
        ClientOptionBuilder()
        .set_key(key)
        .set_secret(secret)
        .set_passphrase(passphrase)
        .set_spot_endpoint(GLOBAL_API_ENDPOINT)
        .set_transport_option(http_transport_option)
        .build()
    )

    # Initialize the client
    client = DefaultClient(client_option)
    return client

def get_market_api(client):
    """
    Retrieves the Spot Market API service from the client.
    
    Args:
        client (DefaultClient): The initialized Kucoin client instance.
    
    Returns:
        MarketAPI: The Spot Market API service.
    """
    return client.rest_service().get_spot_service().get_market_api()