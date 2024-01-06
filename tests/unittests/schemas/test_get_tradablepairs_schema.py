from unittest.mock import Mock, patch
from pydantic import ValidationError
import pytest

from bot.schemas.get_exchangeurls_schema import ExchangeUrlsModel, UrlsListSchema
from bot.schemas.get_tradablepairs_schema import GetTradableAssetPairsSchema


@pytest.fixture
def valid_exchange_urls():
    return ExchangeUrlsModel(
        exchange1=UrlsListSchema(
            base_url="valid_base_url", tradable_pairs="valid_tradable_pairs_url", ohlc_data="valid_ohlc_data_url"
        ),
        exchange2=UrlsListSchema(
            base_url="valid_base_url", tradable_pairs="valid_tradable_pairs_url", ohlc_data="valid_ohlc_data_url"
        ),
    )

# @pytest.fixture
# def valid_binance_asset_pairs_resp_data():



class TestGetTradablePairsSchema:
    def test_instance_creation_ok(self):
        """
        Test that an instance of GetTradableAssetPairsSchema is created successfully.
        """
        # Act
        obj = GetTradableAssetPairsSchema(exchange="binance")

        # Assert
        assert isinstance(obj, GetTradableAssetPairsSchema)

    def test_instance_creation_invalid_exchange(self):
        """
        Test that ValidationError is raised when an invalid exchange is provided.
        """
        # Act and Assert
        with pytest.raises(ValidationError) as context:
            GetTradableAssetPairsSchema(exchange="invalid_exchange")

        assert isinstance(context.value, ValidationError)

    @pytest.mark.parametrize(
        "exchange, json_response",
        [
            ("binance", {"symbols": [{"status": "TRADING", "baseAsset": "BTC", "quoteAsset": "USDT"}]}),
            ("kraken", {"result": {"pair1": {"status": "online", "wsname": "BTC/USDT"}}}),
            ("coinbase", [{"status": "online", "base_currency": "BTC", "quote_currency": "USDT"}]),
        ] 
    )
    @patch('bot.schemas.get_exchangeurls_schema.GetEndpoints.build_tradable_assets_url')
    @patch('bot.schemas.get_tradablepairs_schema.requests.get')
    def test_binance_tradable_pairs(self, mock_requests_get, mock_tradable_assets_url, exchange, json_response):
        """Test correct parsing of json response

        Args:
            mock_requests_get (_type_): mocked function
            mock_tradable_assets_url (_type_): mocked function
            exchange (str): exchange platform
            json_response (dict): response from exchange server
        """
        mock_response = Mock()
        mock_response.json.return_value = json_response
        mock_requests_get.return_value = mock_response
        mock_tradable_assets_url.return_value = "dummy_url"

        # Instantiate your class
        obj = GetTradableAssetPairsSchema(exchange=exchange)
        tradable_pairs = obj.get_tradable_pairs_for_exchange()

        # Assertions
        assert tradable_pairs == ["BTC/USDT"]
        mock_tradable_assets_url.assert_called_once_with()

    @patch('bot.schemas.get_exchangeurls_schema.GetEndpoints.build_tradable_assets_url')
    @patch('bot.schemas.get_tradablepairs_schema.requests.get')
    def test_failed_processing_tradable_pairs_exception_raised(self, mock_requests_get, mock_tradable_assets_url):
        """
        Test that an exception is raised when there is an error fetching tradable pairs.
        """
        # Instantiate your class
        obj = GetTradableAssetPairsSchema(exchange="binance")
        mock_requests_get.side_effect = Exception("An error occurred while fetching tradable pairs")
        mock_tradable_assets_url.return_value = "dummy_url"

        # Mock build_tradable_assets_url to return a dummy URL
        with pytest.raises(Exception) as context:
            obj.get_tradable_pairs_for_exchange()

        assert isinstance(context.value, ValueError) is True
        mock_tradable_assets_url.assert_called_once_with()
