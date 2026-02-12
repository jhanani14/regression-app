FROM python:3.10

WORKDIR /app

# System dependencies
# Workaround for Docker Desktop Mac: Remove problematic apt hooks before update
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    rm -f /etc/apt/apt.conf.d/docker-gzip-indexes && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Disable pip progress bar to avoid threading issues on Mac Docker
ENV PIP_PROGRESS_BAR=off
# Set matplotlib backend to non-GUI to avoid threading issues
ENV MPLBACKEND=Agg
# Disable matplotlib font manager timer to avoid threading issues
ENV MPLCONFIGDIR=/tmp/matplotlib
# Limit OpenBLAS threads to avoid threading issues in Docker Desktop Mac
ENV OPENBLAS_NUM_THREADS=1
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV VECLIB_MAXIMUM_THREADS=1
ENV NUMBA_NUM_THREADS=1

# Upgrade pip
RUN pip install --upgrade --quiet pip setuptools wheel

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install Python deps (no cache)
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Matplotlib temporarily disabled - removed build steps

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]
