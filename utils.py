import pandas as pd
import numpy as np

def trimm_df(df: pd.DataFrame, upper : float, lower: float) -> pd.DataFrame:
    # Trim combined_df using overall quantiles: calculate 2.5% and 97.5% from all values, then remove rows with any value outside
        all_values = df.values.flatten()
        lowerQ = np.quantile(all_values, lower)
        upperQ = np.quantile(all_values, upper)
        mask = (df >= lowerQ) & (df <= upperQ)
        trimmed_df = df[mask.all(axis=1)]
        print(f"Trimmed DataFrame shape: {trimmed_df.shape}")
        
        return trimmed_df