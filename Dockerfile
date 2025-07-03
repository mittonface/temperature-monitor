FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory and log file
RUN mkdir -p data && \
    touch /var/log/cron.log && \
    chmod 0644 /etc/cron.d/collect-data || true

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "run.py"]