@echo off
REM Auto-generated regeneration script for job application
REM Created: 2025-06-25T01:45:45.170160
REM AI Provider: Unknown (Unknown)

echo 🔄 Regenerating job application with same configuration...
echo 📊 Original generation: 2025-06-25T01:45:45.170160
echo 🤖 AI Provider: Unknown (Unknown)

REM Check if we're in the right directory
if not exist "Makefile" (
    echo ❌ Error: Not in project root directory
    echo Please run this script from the Bewerbung project root
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    exit /b 1
)

REM Check virtual environment
if not exist ".venv" (
    echo ⚠️  Virtual environment not found, creating one...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Set environment variables for exact reproduction
set AI_PROVIDER=auto
set OUTPUT_STRUCTURE=by_model
set INCLUDE_GENERATION_METADATA=true

REM Run generation
echo 🚀 Starting generation...
make generate

echo ✅ Regeneration completed successfully!
echo 📁 Check output in: Ausgabe/
echo 🔍 Compare with original using: python tests/test_regeneration.py

pause
