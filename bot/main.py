"""The entry point of the api

Starts the application server with specified server configurations
"""

from fastapi import (
    FastAPI,
)


app = FastAPI()


@app.get("/")
def read_root():
    """The index page for the api"""
    return {"Hello": "World"}
