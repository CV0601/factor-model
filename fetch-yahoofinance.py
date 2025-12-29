#!/usr/bin/env python3

"""

Simple Yahoo Finance data retrieval script using yfinance.



Usage examples (see README.md for full):

  python fetch_yahoo.py --tickers AAPL,MSFT --start 2020-01-01 --end 2023-01-01 --interval 1d --output data.csv

  python fetch_yahoo.py --tickers AAPL --start 2020-01-01 --end 2023-01-01 --output out_dir/

"""

from __future__ import annotations



import argparse

import os

from pathlib import Path

import sys



import pandas as pd

import yfinance as yf





def parse_args() -> argparse.Namespace:

    p = argparse.ArgumentParser(description="Fetch historical data from Yahoo Finance")

    p.add_argument("--tickers", required=True, help="Comma-separated tickers, e.g. AAPL,MSFT")

    p.add_argument("--start", help="Start date YYYY-MM-DD")

    p.add_argument("--end", help="End date YYYY-MM-DD")

    p.add_argument("--interval", default="1d", help="Data interval (1d,1wk,1mo,1m,2m,5m etc)")

    p.add_argument("--output", default="data.csv", help="Output CSV file or directory for per-ticker files")

    p.add_argument("--auto-adjust", action="store_true", help="Auto-adjust prices (split/dividend)")

    return p.parse_args()





def ensure_dir(p: Path) -> None:

    p.mkdir(parents=True, exist_ok=True)





def save_dataframe(df: pd.DataFrame, out: Path) -> None:

    out.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(out, index=True)

    print(f"Saved: {out}")





def flatten_multiindex(df: pd.DataFrame) -> pd.DataFrame:

    if not isinstance(df.columns, pd.MultiIndex):

        return df

    # Flatten columns like ('AAPL','Close') -> 'AAPL_Close'

    df.columns = [f"{c[0]}_{c[1]}" for c in df.columns]

    return df





def fetch_and_save(tickers: list[str], start: str | None, end: str | None, interval: str, output: str, auto_adjust: bool) -> None:

    out_path = Path(output)

    if out_path.is_dir() or output.endswith("/"):

        ensure_dir(out_path)

        for t in tickers:

            print(f"Downloading {t} ...")

            df = yf.download(t, start=start, end=end, interval=interval, auto_adjust=auto_adjust, progress=False)

            if df.empty:

                print(f"Warning: no data for {t}")

                continue

            save_dataframe(df, out_path / f"{t}.csv")

        return



    # Single combined CSV (may contain multiindex columns if multiple tickers)

    print(f"Downloading combined tickers: {','.join(tickers)} ...")

    df = yf.download(tickers, start=start, end=end, interval=interval, auto_adjust=auto_adjust, progress=False)

    if df.empty:

        print("Warning: no data downloaded")

        return

    # If multiple tickers, flatten columns

    df = flatten_multiindex(df)

    save_dataframe(df, out_path)





def main() -> int:

    args = parse_args()

    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]

    if not tickers:

        print("No tickers provided", file=sys.stderr)

        return 2

    fetch_and_save(tickers, args.start, args.end, args.interval, args.output, args.auto_adjust)

    return 0





if __name__ == "__main__":

    raise SystemExit(main())