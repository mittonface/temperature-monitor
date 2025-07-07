#!/usr/bin/env python
"""Add outside humidity column to temperature readings table."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def migrate():
    app = create_app()
    
    with app.app_context():
        # Check if column already exists
        result = db.session.execute(text("PRAGMA table_info(temperature_reading)"))
        columns = [row[1] for row in result]
        
        if 'outside_humidity' not in columns:
            # Add the outside_humidity column
            db.session.execute(text(
                "ALTER TABLE temperature_reading ADD COLUMN outside_humidity FLOAT"
            ))
            db.session.commit()
            print("Successfully added outside_humidity column")
        else:
            print("outside_humidity column already exists")

if __name__ == '__main__':
    migrate()