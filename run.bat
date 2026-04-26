@echo off
title MathPlay Launcher
echo ------------------------------------------------
echo 🚀 MathPlay iske qosyluda...
echo ------------------------------------------------

:: 1. Python check
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Qate: Python ornatylmagan. Otinish, python.org saitynan ornanytynyz.
    pause
    exit
)

:: 2. Venv setup
if not exist "venv" (
    echo 📦 Birinshi ret iske qosyluda. Kitaphanalar ornatyluda...
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

:: 3. Migrate
python manage.py migrate

:: 4. Open browser
start http://127.0.0.1:8000

:: 5. Run server
echo ✅ Sait daiyn! Browser avtomatty turde ashyluy tiis.
echo ------------------------------------------------
python manage.py runserver 0.0.0.0:8000
pause
