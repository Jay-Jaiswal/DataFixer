#!/bin/bash
# Start script for production deployment

echo "🚀 Starting DataFixer API Server..."
echo "📦 Installing dependencies..."

# Install Python dependencies
cd backend
pip install --no-cache-dir -r requirements.txt

echo "🌟 Starting server..."
# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1

echo "✅ Server started successfully!"