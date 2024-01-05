"""This module implements all urls for the various exchange API endpoints"""

from pydantic import BaseModel, field_validator


class UrlsListSchema(BaseModel):
    """
    Pydantic model for storing URLs related to an exchange.

    Attributes:
        base_url (str): The base URL for the exchange.
        ohlc_data (str): The URL endpoint for OHLC (Open, High, Low, Close) data.
        tradable_pairs (str): The URL endpoint for retrieving tradable pairs information.
    """

    base_url: str
    ohlc_data: str
    tradable_pairs: str


class ExchangeUrlsModel(BaseModel):
    """
    Pydantic model for storing exchange URLs.

    Attributes:
        binance (UrlsListSchema): URLs for the Binance exchange.
        coinbase (UrlsListSchema): URLs for the Coinbase exchange.
        kraken (UrlsListSchema): URLs for the Kraken exchange.
    """

    binance: UrlsListSchema = UrlsListSchema(
        base_url="https://api.binance.com/api/v3", ohlc_data="/Ticker?pair=", tradable_pairs="/exchangeInfo"
    )
    coinbase: UrlsListSchema = UrlsListSchema(
        base_url="https://api.exchange.coinbase.com", ohlc_data="", tradable_pairs="/products"
    )
    kraken: UrlsListSchema = UrlsListSchema(
        base_url="https://api.kraken.com/0/public", ohlc_data="", tradable_pairs="/AssetPairs"
    )


class GetEndpoints(ExchangeUrlsModel):
    """
    Block to get endpoints for different exchanges.

    Attributes:
        exchange (str): The name of the exchange.

    Methods:
        build_tradable_assets_url(): Build and return the URL for retrieving tradable assets.
        build_ohlc_assets_url(): Build and return the URL for retrieving OHLC (Open/High/Low/Close) data.
    """

    exchange: str

    @field_validator("exchange")
    def validate_exchange(cls, value):
        """
        Validate the exchange name and convert it to lowercase.

        Args:
            value (str): The provided exchange name.

        Returns:
            (str): The validated and lowercase exchange name.

        Raises:
            ValueError: If the provided exchange name is not one of the supported platforms (binance, coinbase, kraken).
        """
        if value.lower() not in ExchangeUrlsModel.__annotations__.keys():
            raise ValueError(f"Invalid exchange. Supported platforms: {ExchangeUrlsModel.__annotations__.keys()}")
        return value.lower()

    def build_tradable_assets_url(self):
        """
        Build and return the URL for retrieving tradable assets.

        Returns:
            (str): The constructed URL for fetching tradable assets.
        """
        exchange_urls: UrlsListSchema = getattr(self, self.exchange)
        return exchange_urls.base_url + exchange_urls.tradable_pairs

    def build_ohlc_assets_url(self, pair: str, **kwargs):
        """
        Build and return the URL for retrieving OHLC data.

        Returns:
            (str): The constructed URL for fetching OHLC data.
        """
        exchange_urls: UrlsListSchema = getattr(self, self.exchange)
        return exchange_urls.base_url + exchange_urls.ohlc_data + pair
