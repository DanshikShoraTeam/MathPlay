#!/bin/bash
cd "$(dirname "$0")"

echo "------------------------------------------------"
echo " MathPlay iske qosyluda..."
echo "------------------------------------------------"

# Python check
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 tabylmady. python.org-tan ornatyp alynyz!"
    read -p "Enter basып жабыныз..."
    exit 1
fi

# Venv check
if [ ! -f "venv/bin/python" ]; then
    echo "[!] Virtuallik orta joq. Quiluda..."
    python3 -m venv venv
fi

# Install requirements
echo "[!] Kitaphanalar ornatyluda..."
venv/bin/pip install --upgrade pip --quiet
venv/bin/pip install -r requirements.txt --quiet

# Migrate
echo "[!] Malimetter qory daiyndaluda..."
venv/bin/python manage.py migrate

# Browser
echo "[!] Browser ashyluda..."
open http://127.0.0.1:8000

# Run server
echo " Sait daiyn!"
echo "------------------------------------------------"
venv/bin/python manage.py runserver 0.0.0.0:8000