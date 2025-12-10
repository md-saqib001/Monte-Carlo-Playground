from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .simulation import run_monte_carlo
import io
import base64
import matplotlib
matplotlib.use('Agg') # Set backend to non-interactive (Crucial for servers)
import matplotlib.pyplot as plt
from . import db
from .models import Simulation

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # If the user submitted the simulation form
    if request.method == 'POST':
        try:
            # 1. Get data from form
            # Inputs come as strings, so we cast them to float/int
            asset_price = float(request.form.get('price'))
            volatility = float(request.form.get('volatility'))
            
            # 2. Run the Math (Phase 2 Logic)
            # We get the massive matrix of prices
            results = run_monte_carlo(S0=asset_price, sigma=volatility)
            
            # 3. Visualization (The new part)
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot only the first 5 paths (slicing the matrix)
            # results shape is (253, 1000). 
            # results[:, :5] takes all rows, first 5 columns.
            ax.plot(results[:, :5]) 
            
            ax.set_title(f"Monte Carlo Simulation: S0=${asset_price}, Vol={volatility}")
            ax.set_xlabel("Trading Days")
            ax.set_ylabel("Price ($)")
            ax.grid(True)
            
            # 4. Save plot to Memory Buffer (RAM)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0) # Rewind the "cursor" to the start of the file
            plt.close(fig) # Clear memory (Very important!)
            
            # 5. Convert Buffer to Base64 String
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            # 6. Calculate Average Final Price
            final_average = results[-1].mean()

            # Create a new row in the database table
            new_sim = Simulation(
                asset_price=asset_price,
                volatility=volatility,
                average_price=final_average,
                user_id=current_user.id  # Link this run to the logged-in user
            )
            
            # Stage the change
            db.session.add(new_sim)
            
            # Commit (Save) to the file
            db.session.commit()
            
            return render_template("home.html", 
                                   user=current_user, 
                                   image=image_base64,
                                   avg_price=round(final_average, 2),
                                   show_result=True)
                                   
        except ValueError:
            flash('Invalid input. Please enter numbers.', category='error')

    # Default load (no simulation yet)
    return render_template("home.html", user=current_user, show_result=False)