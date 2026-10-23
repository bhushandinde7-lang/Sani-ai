# All-in-One AI Assistant — Starter

Includes an AI chat interface (requires an OpenAI API key in hosting Secrets), a synthetic-data trading dashboard, and a simple EMA backtest for uploaded CSV data.

## Run
`pip install -r requirements.txt`
`streamlit run app.py`

## Deploy
Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository, then deploy on Streamlit Community Cloud with `app.py` as the main file. To enable AI chat, add `OPENAI_API_KEY = "your-key"` in the app's Secrets settings. Never put keys in public code.

## Safety
No live market data, broker integration, or automatic live trading is included. Backtesting is educational and does not model options premiums, expiry, strikes, brokerage, taxes, or slippage.
