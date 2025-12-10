# website/models.py
from . import db  # We will define 'db' in __init__.py shortly
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    # 'id' is the Primary Key: A unique ID for every user (1, 2, 3...)
    id = db.Column(db.Integer, primary_key=True)
    
    # 'unique=True' means no two users can have the same email
    email = db.Column(db.String(150), unique=True)
    
    # We will store a HASH, not the real password. String(150) is enough space for the hash.
    password = db.Column(db.String(150))
    
    first_name = db.Column(db.String(150))
    
    # RELATIONSHIP: This is the "One-to-Many" link.
    # One User has many Simulations.
    # We haven't built the 'Simulation' class yet, so we put it in quotes.
    simulations = db.relationship('Simulation')

# Quick placeholder for Simulation so code doesn't break
class Simulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # Store the Inputs
    asset_price = db.Column(db.Float)
    volatility = db.Column(db.Float)
    
    # Store the Result
    average_price = db.Column(db.Float)
    
    # Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))