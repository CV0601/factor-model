import pandas as pd
from pathlib import Path

def get_portfolio_returns(file_path: str) -> pd.DataFrame:
    """
    Parses an IBKR PortfolioAnalyst CSV and returns a cleaned 
    DataFrame of daily returns.
    """
    target_section = "Time Period Benchmark Comparison"
    #possbile target_section values: "Open Position Summary", etc. more to be added later
    header = None
    data_rows = []

    # 1. Parse the complex CSV structure
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            parts = [element.strip() for element in line.split(',')]
            if parts[0] == target_section:
                if parts[1] == "Header":
                    header = parts
                elif parts[1] == "Data":
                    data_rows.append(parts)

    if not header or not data_rows:
        raise ValueError(f"Could not find the '{target_section}' section in the file.")

    # 2. Create the DataFrame
    df = pd.DataFrame(data_rows, columns=header)
    
    # 3. Identify the Return column (ignores the benchmark BM1 column)
    # This automatically finds your specific Account ID column
    return_col = [c for c in df.columns if c.endswith('Return') and c != 'BM1Return'][0]
    
    # 4. Clean and Convert types
    clean_df = df[['Date', return_col]].copy()
    clean_df.columns = ['Date', 'Portfolio Daily_Return']
    
    # Convert 'Portfolio Daily_Return' to float and 'Date' to datetime
    clean_df['Portfolio Daily_Return'] = pd.to_numeric(clean_df['Portfolio Daily_Return'], errors='coerce')
    # Inspect the Date format by reading the df
    clean_df['Date'] = pd.to_datetime(clean_df['Date'], format='%m/%d/%y')  # Specify format for MM/DD/YY
    
    # Set Date as index (useful for time-series analysis)
    clean_df = clean_df.set_index('Date').sort_index()
    return clean_df
