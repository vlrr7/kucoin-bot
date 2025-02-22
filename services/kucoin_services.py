from kucoin_universal_sdk.generate.spot.market.api_market import MarketAPI
from kucoin_universal_sdk.generate.spot.market.model_get_klines_req import GetKlinesReqBuilder
import logging
from datetime import datetime, timezone, timedelta
import asyncio

def fetch_klines(api: MarketAPI, symbol: str, interval: str, start: datetime, end: datetime):
    """
    # DEPRECATED : USE FETCH_ALL_KLINES INSTEAD
    Fetches historical kline data for a specific symbol.

    Args:
        api (MarketAPI): The market API client instance.
        symbol (str): The trading pair symbol (e.g., 'BTC-USDT').
        interval (str): The kline interval (e.g., '1hour').
        start (int): The start time of the candles to fetch
        end (int): The end time of the candles to fetch

    Returns:
        list: List of kline data (open, high, low, close, volume).
    """
    get_kline_req = (
        GetKlinesReqBuilder()
        .set_symbol(symbol)
        .set_type(interval)
        .set_start_at(int(start.timestamp()))
        .set_end_at(int(end.timestamp()))
        .build()
    )
    kline_resp = api.get_klines(get_kline_req)
    data = kline_resp.data
    real_end = datetime.fromtimestamp(int(data[0][0]), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    real_start = datetime.fromtimestamp(int(data[-1][0]), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Received {len(data)} candles for {symbol} from {real_start} to {real_end}")
    return data

async def fetch_all_klines(api: MarketAPI, symbol: str, interval: str, start_time: datetime, end_time: datetime):
    """
    ### Fetches all kline data for a specific symbol in batches (currently 1500 candles max).
    Order is inversed, only last 1500 candles are returned, so the end time changes at each iteration

    Args:
        api (MarketAPI): The market API client instance.
        symbol (str): The trading pair symbol (e.g., 'BTC-USDT').
        interval (str): The kline interval (e.g., '1min', '1hour').
        start_time (int): Start time in seconds.
        end_time (int): End time in seconds.

    Returns:
        list: List of all kline data.
    """
    all_data = []

    deltat_dict = {
        "1min": timedelta(minutes=1),
        "3min": timedelta(minutes=3),
        "5min": timedelta(minutes=5),
        "15min": timedelta(minutes=15),
        "30min": timedelta(minutes=30),
        "1hour": timedelta(hours=1),
        "2hour": timedelta(hours=2),
        "4hour": timedelta(hours=4),
        "6hour": timedelta(hours=6),
        "8hour": timedelta(hours=8),
        "12hour": timedelta(hours=12),
        "1day": timedelta(days=1),
        "1week": timedelta(days=7),
        "1month": timedelta(days=30)
    }
    deltat = deltat_dict[interval]

    # End time candle is not fetched (ex : if end_time is 15:00, the last candle will be 14:00 in H1)
    current_end_time = end_time + deltat
    

    while current_end_time > start_time:
        try:
            # Fetch a batch of 100 candles
            get_kline_req = (
                GetKlinesReqBuilder()
                .set_symbol(symbol)
                .set_type(interval)
                .set_start_at(int(start_time.timestamp()))
                .set_end_at(int(current_end_time.timestamp()))
                .build()
            )
            kline_resp = api.get_klines(get_kline_req)

            # Append the batch to the full dataset
            all_data.extend(kline_resp.data)

            # Update the start time for the next batch
            last_timestamp = int(kline_resp.data[-1][0])  # Timestamp of the last candle in the batch
            # Because end_time candle is not taken, this is fine, no need to remove a deltat from current_end_time
            current_end_time = datetime.fromtimestamp(last_timestamp, tz=timezone.utc)
            
            logging.info(f"Received {len(kline_resp.data)} candles for {symbol}. Current end time: {current_end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            logging.error(f"Error fetching klines: {e}")
            await asyncio.sleep(31)
            break

    real_end = datetime.fromtimestamp(int(all_data[0][0]), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    real_start = datetime.fromtimestamp(int(all_data[-1][0]), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Received {len(all_data)} candles for {symbol} from {real_start} to {real_end}")

    return all_data