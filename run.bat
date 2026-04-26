@echo off
title MathPlay Launcher
echo ------------------------------------------------
echo 🚀 MathPlay iske qosyluda...
echo ------------------------------------------------

:: 1. Python check
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python tanylmady. Python.org-tan ornatylyp, "Add to PATH" belgilenui tiis!
    pause
    exit
)

:: 2. Venv check
if not exist "venv\Scripts\python.exe" (
    echo [!] Virtuallik orta (venv) tabilmady. Kuriluda...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] Qate: venv quru mumkin bolmady.
        pause
        exit
    )
)

:: 3. Install requirements
echo [!] Kitaphanalardy tekseru (Django, qrcode)...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

:: 4. Double check Django
venv\Scripts\python.exe -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Django ornatylmady. Qaita ornatu...
    venv\Scripts\python.exe -m pip install django pillow qrcode
)

:: 5. Migrate
echo [!] Malimetter qoryn daiyndau...
venv\Scripts\python.exe manage.py migrate

:: 6. Browser
echo [!] Browserdi ashu...
start http://127.0.0.1:8000

:: 7. Run server
echo ✅ Sait daiyn! Browser ashyluy tiis.
echo ------------------------------------------------
venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
pause
