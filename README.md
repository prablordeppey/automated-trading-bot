# automated-trading-bot
This repository contains the source code for an automated trading bot designed to execute trades based on various trading styles and technical indicator strategies. The bot leverages historical market data to optimize parameters and confirm signals, allowing for autonomous decision-making in the dynamic financial markets.

## Key Features:

- **Trading Styles:**
  - Breakout, Trend-Following, Mean-Reversion, Scalping, Swing, and more.
- **Indicator Strategies:**
  - Moving Average Crossover, MACD + Stochastic, Bollinger Bands + RSI, Fibonacci Retracement, Ichimoku Cloud, ADX + DI, and more.
- **Automated Parameter Optimization:**
  - Grid search for optimal parameters using historical data.
- **User Interaction:**
  - Optional user interface for custom parameter input.
- **Risk Management:**
  - Implementation of risk management strategies for capital protection.
- **Logging and Monitoring:**
  - Robust logging system to record trade details and real-time monitoring features.
- **Backtesting:**
  - Validation of strategy effectiveness through backtesting with historical data.

## Usage:

1. Initialize development environment 
  ```bash
    make init_dev_env
  ``` 
1. Setup the local virtual environment
  ```bash
     source ./venv/Scripts/activate
     pip install -r requirements/dev.txt
  ```

## Installing `make`

1. Install `choco` via powershell to install `make`.
   ```cmd
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
1. Install `make` via
   ```cmd
   choco install make
   ```
1. Restart your terminal to pickup changes
1. run `make` to list all available targets/commands.


## Disclaimer:

This trading bot is provided for educational and experimental purposes only. Use it at your own risk. The authors and contributors are not responsible for any financial losses incurred.
