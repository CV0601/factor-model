import pytest
import pandas as pd
import os
from fetch_portfolio_data import get_portfolio_returns  # <--- Change this to your actual filename

# 1. Test if the file exists before starting
def test_file_exists():
    assert os.path.exists("data_22_12_2025.csv"), "The IBKR CSV file is missing!"

# 2. Test if the function returns the correct structure
def test_dataframe_structure():
    df = get_portfolio_returns("data_22_12_2025.csv")
    
    # Check if it's a DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check if 'Daily_Return' column exists
    assert "Daily_Return" in df.columns
    
    # Check if the index is a DatetimeIndex
    assert isinstance(df.index, pd.DatetimeIndex)

# 3. Test data integrity (Logic Check)
def test_data_values():
    df = get_portfolio_returns("data_22_12_2025.csv")
    
    # Check if returns are within a realistic range (e.g., no 10,000% days)
    # 1.0 = 100% gain in one day
    assert df["Daily_Return"].max() < 1.0
    assert df["Daily_Return"].min() > -1.0
    
    # Check that we actually have data (should be hundreds of rows)
    assert len(df) > 0