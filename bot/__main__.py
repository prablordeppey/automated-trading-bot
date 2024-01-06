"""Serve the application
"""

import uvicorn


if __name__ == "__main__":
    config = uvicorn.Config(
        "bot.main:app", host="0.0.0.0", port=5000, log_level="info", reload=True, reload_dirs=["bot"]
    )
    server = uvicorn.Server(config)
    server.run()
