# client_setup.py
import os
from kucoin_universal_sdk.api.client import DefaultClient
from kucoin_universal_sdk.model.client_option import ClientOptionBuilder
from kucoin_universal_sdk.model.constants import GLOBAL_API_ENDPOINT
from kucoin_universal_sdk.model.transport_option import TransportOptionBuilder

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