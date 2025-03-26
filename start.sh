#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Run database initialization
python init_db.py

# Start the application
uvicorn src.main:app --host 0.0.0.0 --port 8000 