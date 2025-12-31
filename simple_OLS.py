import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt

def perform_ols_analysis(df):
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
        "mse": model.mse_resid
    }
    
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

    # --- Plot 1: Actual vs. Predicted with Coefficients ---
    ax1.scatter(model.fittedvalues, y, alpha=0.5, color='royalblue', label='Data Points')
    line_coords = [y.min(), y.max()]
    ax1.plot(line_coords, line_coords, color='red', linestyle='--', label='Perfect Fit')
    
    # Adding the coefficient text box
    ax1.text(0.05, 0.95, coef_text, transform=ax1.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    
    ax1.set_title(f'Actual vs. Predicted (R²: {model.rsquared:.3f})')
    ax1.set_xlabel('Predicted')
    ax1.set_ylabel('Actual')
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

# --- How to run this in your Notebook tab ---
# model, stats = perform_ols_analysis(combined_df)
# print(stats["r_squared"]) # Access individual metrics
# print(model.summary())    # See the full table