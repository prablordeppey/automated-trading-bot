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

    def test_exchange_urls_fields_exist(self):
        """This test implements:
        - expected exchanges exist
        - exchanges do not have empty urls
        """
        # Prepare
        expected_exchanges = ["binance", "kraken", "coinbase"]

        # Act
        exchanges = ExchangeUrlsModel()
        exchanges_dict = exchanges.__annotations__

        # Assert
        assert set(expected_exchanges) == set(exchanges_dict.keys())
        for exchange in expected_exchanges:
            exchange_data = getattr(exchanges, exchange)
            exchange_data_dict = getattr(exchanges, exchange).__annotations__
            for url in exchange_data_dict.keys():
                assert getattr(exchange_data, url) != ""

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

    def test_build_ohlc_assets_url(self):
        """TODO: Poorly written, build around business logic"""
        # Act
        res_binance = GetEndpoints(exchange="binance")
        result_binance = res_binance.build_ohlc_assets_url(pair="BTC-USDT")

        res_coinbase = GetEndpoints(exchange="coinbase")
        result_coinbase = res_coinbase.build_ohlc_assets_url(pair="BTC-USDT")

        # Assert
        assert isinstance(result_binance, str) is True
        assert isinstance(result_coinbase, str) is True
