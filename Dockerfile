FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync  

# Copy application code
COPY src/ ./src/
COPY init_db.py ./
COPY start.sh ./
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the startup script
CMD ["./start.sh"]
