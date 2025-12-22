# 1️⃣ Use lightweight Python image
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install system dependencies (IMPORTANT for matplotlib & psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy requirements first (for caching)
COPY requirements.txt .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy application code
COPY . .

# 7️⃣ Expose port
EXPOSE 8000

# 8️⃣ Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
