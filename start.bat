@echo off
REM Start script for Windows production deployment

echo 🚀 Starting DataFixer API Server...
echo 📦 Installing dependencies...

REM Install Python dependencies
cd backend
pip install --no-cache-dir -r requirements.txt

echo 🌟 Starting server...
REM Start the server
python -m uvicorn main:app --host 0.0.0.0 --port %PORT% --workers 1

echo ✅ Server started successfully!
pause