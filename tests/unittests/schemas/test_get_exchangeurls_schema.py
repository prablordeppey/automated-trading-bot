import pytest

from bot.schemas.get_exchangeurls_schema import ExchangeUrlsModel, GetEndpoints, UrlsListSchema


class TestGetExchangeUrlsSchema:
    def test_essential_url_fields_exist(self):
        # Prepare
        expected_urls = ["base_url", "ohlc_data", "tradable_pairs"]

        # Act
        urls = UrlsListSchema.__annotations__.keys()

        # Assert
        assert len(urls) == 3
        assert set(expected_urls) == set(urls)

    @pytest.mark.parametrize(
        "exchange, expected_response",
        [
            ("binance", "binance"),
            ("kraken", "kraken"),
            ("coinbase", "coinbase"),
        ],
    )
    def test_get_endpoint_validate_exchange_ok(self, exchange, expected_response):
        """TODO: Improve this with mocking. business case instead of checking the returns"""
        # Prepare
        # Act
        result = GetEndpoints(exchange=exchange)

        # Assert
        assert result.exchange == expected_response

    def test_get_endpoint_validate_exchange_fail(self):
        """TODO: Improve this with mocking"""
        # Act
        with pytest.raises(ValueError):
            GetEndpoints(exchange="invalid_exchange")

    def test_build_tradable_assets_url(self):
        """TODO: build around business logic"""
        # Act
        res_obj = GetEndpoints(exchange="binance")
        result = res_obj.build_tradable_assets_url()

        # Assert
        assert isinstance(result, str) is True

