#!/bin/bash
# Robust deployment startup script

echo "🚀 Starting DataFixer API..."

# Set working directory
cd backend

# Check Python version
echo "📋 Python version: $(python --version)"

# Install dependencies with fallback
echo "📦 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt || {
    echo "⚠️  Main requirements failed, trying minimal install..."
    pip install --no-cache-dir -r requirements-minimal.txt || {
        echo "🔄 Fallback: Installing core dependencies individually..."
        pip install --no-cache-dir fastapi uvicorn pandas numpy python-multipart requests
    }
}

# Check if critical modules are available
echo "🔍 Checking critical imports..."
python -c "import fastapi, uvicorn, pandas, numpy; print('✅ Core dependencies OK')" || {
    echo "❌ Critical dependencies missing!"
    exit 1
}

# Optional: Check ydata-profiling
python -c "import ydata_profiling; print('✅ ydata-profiling available')" 2>/dev/null || {
    echo "⚠️  ydata-profiling not available (this is OK)"
}

echo "🌟 Starting server..."
exec python -m uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}