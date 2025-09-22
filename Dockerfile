# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000
ENV ENV=production

# Install system dependencies required for pandas and other packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        gcc \
        g++ \
        gfortran \
        libopenblas-dev \
        liblapack-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements first (for better Docker layer caching)
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies with fallback
RUN pip install --no-cache-dir -r requirements.txt || \
    (echo "Main requirements failed, trying minimal..." && \
     pip install --no-cache-dir fastapi uvicorn[standard] pandas numpy python-multipart requests)

# Copy backend code
COPY backend/ /app/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]