#!/usr/bin/env python
"""Script to manually collect temperature data from Nest."""
from dotenv import load_dotenv
load_dotenv()

from app.nest_client import collect_temperature_data

if __name__ == '__main__':
    collect_temperature_data()