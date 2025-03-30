help:
    just --list

# Run the app with the specified environment.
run *ENV:
    ENV={{ ENV }} uv run python -m uvicorn src.main:app --reload

# Run ruff format
fmt:
    uvx ruff format

# Run ruff check
lint:
    uvx ruff check --fix

# Run mypy
mypy:
    uv run mypy src