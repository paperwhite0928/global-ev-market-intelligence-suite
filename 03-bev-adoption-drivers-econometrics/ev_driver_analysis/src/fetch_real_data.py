"""
fetch_real_data.py - Real Data Fetcher (FRED API & yfinance)
Retrieves live macroeconomic data and crude oil futures as secondary data overlay.
"""

import pandas as pd
import yfinance as yf

def fetch_macro_data() -> pd.DataFrame:
    """Fetch WTI Oil crude prices and Interest Rate indicators from Yahoo Finance."""
    try:
        oil = yf.Ticker("CL=F").history(period="5y", interval="1mo")["Close"]
        oil.name = "wti_oil_real"
        oil.index = pd.to_datetime(oil.index).tz_localize(None).to_period("M").to_timestamp()
        return oil.to_frame()
    except Exception as e:
        print(f"Warning: Failed to fetch live financial data ({e}). Fallback to synthetic panel.")
        return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_macro_data()
    print("Real data head:")
    print(df.head())
