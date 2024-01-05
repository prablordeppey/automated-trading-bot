"""This module aims for fetching tradable pairs data for a given exchange. 

It inherits from the GetEndpoints class, which provides the
endpoint URLs for the specified exchange.

Classes:
    GetAssetPairsOHLCDataSchema: A class to fetch tradable pairs data for a given exchange.

Attributes:
    endpoint (str): The endpoint for fetching OHLC (Open/High/Low/Close) data.

Methods:
    get_tradable_pairs_for_exchange(): Fetch a list of tradable pairs for the specified exchange.
"""

import requests
import pandas as pd

from bot.schemas.get_exchangeurls_schema import GetEndpoints


class GetTradableAssetPairsSchema(GetEndpoints):
    """
    A class to fetch tradable pairs data for a given exchange.

    Attributes:
        exchange (str): The exchange/platform.

    Methods:
        get_tradable_pairs_for_exchange(): Fetch a list of tradable pairs for the specified exchange.
    """

    def __init__(self, exchange: str):
        """
        Args:
            exchange (str): The exchange/platform to fetch assets data.
        """
        super().__init__(exchange=exchange)

    def get_tradable_pairs_for_exchange(self) -> list:
        """
        Get a list of tradable pairs for a given exchange.

        Returns:
            (list[str]): tradable pairs with each format <BASE>/<QUOTE>.
        """
        tradable_pairs: list[str] = []

        # Build the endpoint URL for retrieving pairs information
        pairs_info_url = self.build_tradable_assets_url()

        # Make a GET request to the endpoint
        resp = requests.get(pairs_info_url)

        try:
            # Process the response based on the exchange
            if self.exchange == "binance":
                df = pd.DataFrame(resp.json()["symbols"])
                tradable_pairs = df[df.status == "TRADING"].reset_index()
                tradable_pairs["pair_name"] = tradable_pairs.apply(lambda x: x.baseAsset + "/" + x.quoteAsset, axis=1)
                tradable_pairs = tradable_pairs.pair_name.to_list()
            elif self.exchange == "kraken":
                df = pd.DataFrame(resp.json()["result"]).T
                tradable_pairs = df[df.status == "online"].wsname.to_list()
            elif self.exchange == "coinbase":
                df = pd.DataFrame(resp.json())
                tradable_pairs = df[df.status == "online"]
                tradable_pairs["pair_name"] = tradable_pairs.apply(
                    lambda x: x.base_currency + "/" + x.quote_currency, axis=1
                )
                tradable_pairs = tradable_pairs.pair_name.to_list()
        except Exception as e:
            print("an error occured:", e)

        print(f"Found {len(tradable_pairs)} tradable pairs ...")

        return tradable_pairs
