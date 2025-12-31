import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def perform_ols_analysis(df, graphs=False):
    """
    y = Column 0, X = All other columns.
    Returns model and results dictionary. 
    Displays Diagnostic Plots with Coefficients included.
    """
    y = df.iloc[:, 0]
    X = df.iloc[:, 1:]
    X_with_intercept = sm.add_constant(X)
    
    # 1. Fit the model
    model = sm.OLS(y, X_with_intercept).fit()
    
    # 2. Extract results
    results_dict = {
        "coefficients": model.params,
        "t_stats": model.tvalues,
        "r_squared": model.rsquared,
        "adj_r_squared": model.rsquared_adj,
        "mse": model.mse_resid,
        "residuals": model.resid
    }
    if graphs: # Display diagnostic plots
        # 3. Format coefficients for the plot
        # We'll grab the intercept and the first few coefficients
        coef_text = f"Intercept: {model.params[0]:.4f}\n"
        for i, val in enumerate(model.params[1:], 1):
            coef_text += f"β{i} ({df.columns[i]}): {val:.4f}\n"
            if i >= 3: # Stop after 3 variables so the graph isn't crowded
                coef_text += "..." 
                break

        # 4. Diagnostic Plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # --- Plot 1: Portfolio vs. Market with Coefficients ---
        ax1.scatter(X_with_intercept.iloc[:, 1], y, alpha=0.5, color='royalblue', label='Data Points')
        # Create 100 points from the min to max of the market
        x_range = np.linspace(X_with_intercept.iloc[:, 1].min(), X_with_intercept.iloc[:, 1].max(), 100)
        y_line = model.params[0] + (model.params[1] * x_range)
        ax1.plot(x_range, y_line, color='red', lw=2, label=f'Beta: {model.params[1]:.2f}')
        # Adding the coefficient text box
        ax1.text(0.05, 0.95, coef_text, transform=ax1.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
        
        ax1.set_title(f'Actual vs. Predicted (R²: {model.rsquared:.3f})')
        ax1.set_xlabel('Market Returns')
        ax1.set_ylabel('Portfolio Returns')
        ax1.legend(loc='lower right')

        # --- Plot 2: Residual Plot ---
        ax2.scatter(model.fittedvalues, model.resid, alpha=0.5, color='teal')
        ax2.axhline(y=0, color='red', linestyle='--')
        ax2.set_title('Residuals vs. Fitted')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Residuals')

        plt.tight_layout()
        plt.show()
    
    return model, results_dict

def run_monthly_regressions(df, graphs_overtime=False, EDA_graphs=False):
    """
    Perform OLS regressions for each month in the DataFrame.
    Returns a DataFrame with monthly coefficients, t-stats, R², and N.
    """
    monthly_results = []
    
    for timestamp, month_data in df.groupby(pd.Grouper(freq='ME')):
        if len(month_data) > 15:
            model, stats = perform_ols_analysis(month_data, graphs=EDA_graphs)
            
            # Create a flat dictionary for this month's row
            row = {'month': timestamp, 'N': len(month_data), 'R2': stats['r_squared']}
            
            # Dynamically add Betas and T-Stats for every column
            for col_name in stats['coefficients'].index:
                row[f'{col_name}_beta'] = stats['coefficients'][col_name]
                row[f'{col_name}_tstat'] = stats['t_stats'][col_name]
            
            monthly_results.append(row)
            print(f"Processed {timestamp.strftime('%B %Y')}")
            
    # Create the DataFrame once at the end
    history_df = pd.DataFrame(monthly_results).set_index('month')
    if graphs_overtime:
        plot_all_coefficients(history_df)
        
    return history_df

def plot_all_coefficients(history_df):
    """_summary_
    Plots the evolution of all coefficients over time.
    Args:
        history_df (_type_): pandas DataFrame with monthly regression results.

    Returns:
        _type_: pandas DataFrame with monthly coefficients.
    """
    # 1. Identify all beta columns (including const_beta)
    all_beta_cols = [c for c in history_df.columns if c.endswith('_beta')]
    
    if not all_beta_cols:
        return print("No coefficients found in the DataFrame.")
    
    plt.figure(figsize=(14, 7))    
    for col in all_beta_cols:
        clean_name = col.replace('_beta', '')
        # We use a distinct style for the Constant if it exists
        if clean_name == 'const':
            plt.plot(history_df.index, history_df[col], label='Intercept (Constant)', 
                     linestyle='--', color='black', linewidth=1.5, alpha=0.7)
        else:
            plt.plot(history_df.index, history_df[col], marker='o', label=f'Beta: {clean_name}', 
                     linewidth=2)

    # 3. Add a baseline at zero
    plt.axhline(y=0, color='red', linestyle='-', alpha=0.2, linewidth=1)
    
    # 4. Styling and Formatting
    plt.title('Monthly Coefficient Evolution (All Variables)', fontsize=15, pad=20)
    plt.xlabel('Timeline', fontsize=12)
    plt.ylabel('Market Beta', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.5)
    
    # Place legend outside the plot area so it doesn't cover the lines
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)
    
    plt.tight_layout()
    plt.show()

# --- RUN IT ---
# beta_trends = run_monthly_regressions(combined_df)
