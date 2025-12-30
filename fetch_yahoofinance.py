#!/usr/bin/env python3

"""

Simple Yahoo Finance data retrieval script using yfinance.



Usage examples (see README.md for full):

  python fetch_yahoo.py --tickers AAPL,MSFT --start 2020-01-01 --end 2023-01-01 --interval 1d --output data.csv

  python fetch_yahoo.py --tickers AAPL --start 2020-01-01 --end 2023-01-01 --output out_dir/

"""

import pandas as pd
import yfinance as yf

def flatten_multiindex(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten MultiIndex columns in a DataFrame by joining levels with underscores.

    For DataFrames with MultiIndex columns (e.g., from yfinance downloads with multiple tickers),
    this converts tuples like ('AAPL', 'Close') to flat strings like 'AAPL_Close'.

    Args:
        df: Input DataFrame, potentially with MultiIndex columns.

    Returns:
        pd.DataFrame: DataFrame with flattened column names if MultiIndex was present,
                      otherwise the original DataFrame.
    """
    if not isinstance(df.columns, pd.MultiIndex):
        return df
    # Flatten columns like ('AAPL','Close') -> 'AAPL_Close'
    df.columns = [f"{c[0]}_{c[1]}" for c in df.columns]
    return df

def fetch_data(tickers, start=None, end=None, interval='1d', auto_adjust=False):
    """
    Fetch historical data from Yahoo Finance and return as DataFrame.

    Args:
        tickers: List of ticker symbols or comma-separated string
        start: Start date (YYYY-MM-DD)
        end: End date (YYYY-MM-DD)
        interval: Data interval (1d,1wk,1mo, etc.)
        auto_adjust: Whether to auto-adjust prices

    Returns:
        pd.DataFrame: Historical data
    """
    if isinstance(tickers, str):
        tickers = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if not tickers:
        raise ValueError("No tickers provided")
    
    print(f"Downloading combined tickers: {','.join(tickers)} ...")
    df = yf.download(tickers, start=start, end=end, interval=interval, auto_adjust=auto_adjust, progress=False)
    if df.empty:
        raise ValueError("No data downloaded")
    # If multiple tickers, flatten columns
    df = flatten_multiindex(df)
    return df

