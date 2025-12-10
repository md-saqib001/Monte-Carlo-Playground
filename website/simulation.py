import numpy as np

def run_monte_carlo(S0, sigma, T=1, r=0.05, simulations=1000, steps=252):
    """
    S0: Initial Stock Price
    sigma: Volatility (e.g., 0.2 for 20%)
    T: Time in years
    r: Risk-free rate
    simulations: Number of paths to generate
    steps: Number of trading days in a year (usually 252)
    """
    
    dt = T / steps
    
    # ARRAY MATH (Vectorization) - This is what seniors look for.
    # Instead of looping 1000 times, we create a massive matrix of random numbers at once.
    # shape = (steps + 1, simulations)
    
    # 1. Generate random shocks (Z)
    Z = np.random.normal(0, 1, (steps, simulations))
    
    # 2. Create the price path matrix
    price_matrix = np.zeros((steps + 1, simulations))
    price_matrix[0] = S0
    
    # 3. Calculate the path step-by-step
    # Formula: S_t = S_{t-1} * exp( (r - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z )
    for t in range(1, steps + 1):
        price_matrix[t] = price_matrix[t-1] * np.exp(
            (r - 0.5 * sigma**2) * dt + 
            sigma * np.sqrt(dt) * Z[t-1]
        )
        
    return price_matrix