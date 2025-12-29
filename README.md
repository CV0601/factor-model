# factor-model
This is an attempt to create a factor model environment, it will include the following:
1. Data Retrieval - Yahoo Finance script available (`yahoo_finance_data.py`)
2. Factor Creation
3. Factor Selection (Dimension Reduction)
4. Estimate Factor Loadings to Portfolio
5. Reporting (package not yet determined)

The structure is yet to be determined. As I start experimenting and incorporating the methods could change or data source/structure could change.

## Data Retrieval

To retrieve historical stock data from Yahoo Finance, use the `yahoo_finance_data.py` script:

```bash
pip install -r requirements.txt
python yahoo_finance_data.py --ticker AAPL --period 1y --output aapl_data.csv
```

This will download 1 year of historical data for AAPL and save it to `aapl_data.csv`.

Packages on requirements.txt : 
Numpy
scikitlearn
pandas

