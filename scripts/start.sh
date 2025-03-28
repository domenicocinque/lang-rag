#!/bin/bash

set -e 
set -x  

# Run database initialization
uv run python -m src.init_db

# Start the application
uv run python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 