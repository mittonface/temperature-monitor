#!/usr/bin/env python
"""Add outside temperature columns to the database."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from sqlalchemy import text

def add_outside_temperature_columns():
    app = create_app()
    
    with app.app_context():
        try:
            # Add the new columns
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE temperature_reading ADD COLUMN outside_temperature_c REAL"))
                conn.execute(text("ALTER TABLE temperature_reading ADD COLUMN outside_temperature_f REAL"))
                conn.commit()
            
            print("Successfully added outside temperature columns")
        except Exception as e:
            print(f"Error adding columns: {e}")
            print("Columns may already exist")

if __name__ == '__main__':
    add_outside_temperature_columns()