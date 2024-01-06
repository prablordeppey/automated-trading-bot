"""This module implements all urls for the various exchange API endpoints"""

from pydantic import BaseModel, field_validator


class UrlsListSchema(BaseModel):
    """
    Pydantic model for storing URLs related to an exchange.

    Attributes:
        base_url (str): The base URL for the exchange.
        ticker (str): The URL endpoint for OHLC (Open, High, Low, Close) data.
        asset_pairs (str): The URL endpoint for retrieving tradable pairs information.
    """

    base_url: str
    ticker: str
    asset_pairs: str


class ExchangeUrlsModel(BaseModel):
    """
    Pydantic model for storing exchange URLs.

    https://binance-docs.github.io/apidocs/spot/en/#rolling-window-price-change-statistics
    https://support.kraken.com/hc/en-us/articles/360000920306-API-symbols-and-tickers
    https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproducts

    Attributes:
        binance (UrlsListSchema): URLs for the Binance exchange.
        coinbase (UrlsListSchema): URLs for the Coinbase exchange.
        kraken (UrlsListSchema): URLs for the Kraken exchange.
    """

    binance: UrlsListSchema = UrlsListSchema(
        base_url="https://api.binance.com/api/v3",
        ticker="/ticker?symbols=",
        kline="/klines?",
        asset_pairs="/exchangeInfo?",
    )
    coinbase: UrlsListSchema = UrlsListSchema(
        base_url="https://api.exchange.coinbase.com",
        ticker="products/%s/ticker",
        kline="products/%s/candles?",
        asset_pairs="/products?",
    )
    kraken: UrlsListSchema = UrlsListSchema(
        base_url="https://api.kraken.com/0/public", ticker="/Ticker?pair=", kline="", asset_pairs="/AssetPairs"
    )
    bybit: UrlsListSchema = UrlsListSchema(
        base_url="https://api-testnet.bybit.com/v5",
        ticker="/market/tickers",
        kline="/market/kline?",
        asset_pairs="/market/instruments-info?",
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
            raise ValueError(
                f"Invalid exchange. Supported platforms: {ExchangeUrlsModel.__annotations__.keys()} but given {value}."
            )
        return value.lower()

    def build_tradable_assets_url(self, **kwargs):
        """
        Build and return the URL for retrieving tradable assets.

        Returns:
            (str): The constructed URL for fetching tradable assets.
        """
        exchange_urls: UrlsListSchema = getattr(self, self.exchange)
        parsed_endpoint = exchange_urls.base_url + exchange_urls.asset_pairs
        if kwargs:
            parsed_endpoint += "&".join(f"{key}={value}" for key, value in kwargs.items())
        return parsed_endpoint

    def build_ohlc_assets_url(self, pair: str):
        """
        Build and return the URL for retrieving OHLC data.
        TODO: improve to accept kwargs to build url

        Returns:
            (str): The constructed URL for fetching OHLC data.
        """
        exchange_urls: UrlsListSchema = getattr(self, self.exchange)

        if self.exchange == "coinbase":
            return exchange_urls.base_url + exchange_urls.ticker.format(pair)

        return exchange_urls.base_url + exchange_urls.ticker + pair
