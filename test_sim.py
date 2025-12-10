from website.simulation import run_monte_carlo

# Run a test simulation
print("Running simulation...")
results = run_monte_carlo(S0=100, sigma=0.2)

# Check the shape (Should be 253 rows, 1000 columns)
print(f"Shape of result: {results.shape}")

# Check the final average price (Should be close to 100 * e^(0.05) ≈ 105.1)
final_prices = results[-1] # Get the last row
average_price = final_prices.mean()
print(f"Average final price: ${average_price:.2f}")

# Sanity Check: No negative prices
print(f"Min price seen: {results.min()}")