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

from typing import List
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

    def __get_binance_tradable_pairs(self, df: pd.DataFrame) -> List[str]:
        """Binance tradable pairs"""
        tradable_pairs = df[df.status == "TRADING"].reset_index()
        tradable_pairs["pair_name"] = tradable_pairs.apply(lambda x: x.baseAsset + "/" + x.quoteAsset, axis=1)
        tradable_pairs = tradable_pairs.pair_name.to_list()
        return tradable_pairs

    def __get_kraken_tradable_pairs(self, df: pd.DataFrame) -> List[str]:
        """Kraken tradable pairs"""
        tradable_pairs = df[df.status == "online"].wsname.to_list()
        return tradable_pairs

    def __get_coinbase_tradable_pairs(self, df: pd.DataFrame) -> List[str]:
        """Coinbase tradable pairs"""
        tradable_pairs = df[df.status == "online"]
        tradable_pairs["pair_name"] = tradable_pairs.apply(lambda x: x.base_currency + "/" + x.quote_currency, axis=1)
        tradable_pairs = tradable_pairs.pair_name.to_list()
        return tradable_pairs

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
        try:
            resp = requests.get(pairs_info_url).json()

            # Process the response based on the exchange
            if self.exchange == "binance":
                tradable_pairs = pd.DataFrame(resp["symbols"]).pipe(self.__get_binance_tradable_pairs)
            elif self.exchange == "kraken":
                tradable_pairs = pd.DataFrame(resp["result"]).T.pipe(self.__get_kraken_tradable_pairs)
            elif self.exchange == "coinbase":
                tradable_pairs = pd.DataFrame(resp).pipe(self.__get_coinbase_tradable_pairs)
        except Exception as e:
            print(f"An error occurred while fetching tradable pairs: {e}")
            raise ValueError("An error occurred while fetching tradable pairs")

        print(f"Found {len(tradable_pairs)} tradable pairs ...")

        return tradable_pairs
