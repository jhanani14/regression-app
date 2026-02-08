FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libstdc++6 \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first (VERY important)
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install Python deps (no cache)
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
