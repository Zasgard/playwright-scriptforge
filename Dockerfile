FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium firefox webkit

# Copy application code
COPY . .

# Make CLI executable
RUN chmod +x /app/scriptforge.py

# Set entrypoint
ENTRYPOINT ["python", "/app/scriptforge.py"]
CMD ["--help"]
