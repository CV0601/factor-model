#!/usr/bin/env python3
"""
Main entry point for the factor model analysis.

Structure:
1. Data fetching: Retrieve portfolio and market data
2. Data handling: Preprocess and merge data
3. Factor analysis: Run LASSO regression or other models
4. Reporting: Generate outputs (console, files, etc.)
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from fetch_portfolio_data import get_portfolio_returns
from fetch_yahoofinance import fetch_data
import matplotlib
import simple_OLS
# from analysis import run_factor_analysis  # To be created
# from reporting import generate_report  # To be created

def main():
    # Step 1: Data Fetching
    print("Step 1: Fetching data...")
    try:
        # Portfolio data from CSV using function
        data_dir = Path('data')
        csv_file = data_dir / 'data_22_12_2025.csv'
        portfolio_df = get_portfolio_returns(str(csv_file))
        print(f"Fetched portfolio data with shape: {portfolio_df.shape}")

        # Set start and end dates based on portfolio data
        start_date = portfolio_df.index.min().strftime('%Y-%m-%d')
        end_date = portfolio_df.index.max().strftime('%Y-%m-%d')
        print(f"Using date range: {start_date} to {end_date}")

        # Market data
        market_df = fetch_data(
            tickers='^990100-USD-STRD',  # msci world index
            start=start_date,
            end=end_date,
            interval='1d',
            auto_adjust=True
        )
        print(f"Fetched market data with shape: {market_df.shape}")
    except Exception as e:
        print(f"Error in data fetching: {e}")
        sys.exit(1)

    # Step 2: Data Handling
    print("Step 2: Handling data...")
    try:
        # Calculate returns for market data
        adj_market_df = market_df.pct_change()*100
        # Align market_df to portfolio_df dates (portfolio is master)
        common_dates = portfolio_df.index.intersection(adj_market_df.index)
        portfolio_df = portfolio_df.loc[common_dates]
        adj_market_df = adj_market_df.loc[common_dates]
        print(f"Aligned data to common dates. Portfolio shape: {portfolio_df.shape}, Market shape: {adj_market_df.shape}")

        # Filter adj_market_df to keep only 'Close' columns
        adj_market_df = adj_market_df.filter(like='Close', axis=1)

        print(f"Filtered market_df to Close columns. Shape: {adj_market_df.shape}")

        # Combine portfolio_df and adj_market_df
        combined_df = pd.concat([portfolio_df, adj_market_df], axis=1).dropna()
        print(f"Combined DataFrame shape: {combined_df.shape}")

        # Trim combined_df using overall quantiles: calculate 2.5% and 97.5% from all values, then remove rows with any value outside
        all_values = combined_df.values.flatten()
        lower = np.quantile(all_values, 0.025)
        upper = np.quantile(all_values, 0.975)
        mask = (combined_df >= lower) & (combined_df <= upper)
        processed_df = combined_df[mask.all(axis=1)]
        print(f"Trimmed DataFrame shape: {processed_df.shape}")
    except Exception as e:
        print(f"Error in data handling: {e}")
        sys.exit(1)

    # Step 3: Factor Analysis
    print("Step 3: Running factor analysis...")
    try:
        model, stats = simple_OLS.perform_ols_analysis(processed_df)
        print(f"Analysis complete. Sample results: {stats}")
    except Exception as e:
        print(f"Error in factor analysis: {e}")
        sys.exit(1)

    # Step 4: Reporting
    print("Step 4: Generating report...")
    try:
        # generate_report(results, output_path='output/report.txt')
        print("Report: Analysis results printed to console.")
        print(stats)  # Placeholder
    except Exception as e:
        print(f"Error in reporting: {e}")
        sys.exit(1)

    print("Pipeline complete!")

if __name__ == "__main__":
    main()