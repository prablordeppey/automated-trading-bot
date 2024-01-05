"""The entry point of the api

Starts the application server with specified server configurations
"""

from fastapi import FastAPI, HTTPException, status
from bot.schemas.get_tradablepairs_schema import GetTradableAssetPairsSchema

app = FastAPI()


@app.get("/")
def read_root():
    """The index page for the api"""
    return {"Hello": "World"}


@app.get("/scan-tradable-asset-pairs", response_model=dict, status_code=status.HTTP_200_OK)
def tradable_asset_pairs(exchange: str) -> dict:
    """
    Get a list of tradable asset pairs for a specified exchange.

    Args:
        exchange (str): The name of the exchange (e.g., "binance" or "kraken").

    Returns:
        (dict): The length and list of tradable pairs.
            Example: {"length": 10, "tradable_pairs": ["BTC/USD", "ETH/BTC", ...]}
    """
    try:
        # Get tradable pairs for the specified exchange
        tradable_pairs = GetTradableAssetPairsSchema(exchange=exchange).get_tradable_pairs_for_exchange()

        # Return the response
        return {"length": len(tradable_pairs), "tradable_pairs": tradable_pairs}

    except Exception as e:
        # Handle exceptions and return appropriate HTTP response
        raise HTTPException(status_code=500, detail=f"Error retrieving tradable asset pairs: {str(e)}")
