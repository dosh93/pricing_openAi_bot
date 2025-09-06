# Telegram OpenAI Pricing Bot

This bot calculates the price of OpenAI requests in Russian rubles.

## Commands

- `/set_prices <input_price_usd> <output_price_usd>` — set prices for input and output tokens in USD per 1M tokens.
- `/set_rate <usd_to_rub>` — set the USD to RUB exchange rate.
- `/calc <input_tokens> <output_tokens>` — calculate cost in RUB.

## Local run

```bash
pip install -r requirements.txt
BOT_TOKEN=<your token> python bot.py
```

## Docker

1. Copy `.env.example` to `.env` and put your Telegram bot token there.
2. Start the bot:

```bash
docker-compose up --build
```
