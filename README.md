# MLeng-PT: Machine Learning Engineering Project

A Python-based application for conducting similarity searches and retrieving similar pairs from a dataset.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 

## Installation

1. Clone the repository:

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Bonus) If you use `uv` as your package manager, you can install the dependencies with:
```bash
uv sync
```

## Setup

1. Start the PostgreSQL database using Docker Compose:
```bash
docker-compose up -d
```

2. Initialize the database:
```bash
python init_db.py
```

## Running the Application

1. Start the application:
```bash
python -m uvicorn src.main:app
```

or `just run dev` if you have `just` installed.

The API documentation will be available at `http://localhost:8000/docs`

