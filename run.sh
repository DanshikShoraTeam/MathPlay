#!/bin/bash

echo "------------------------------------------------"
echo "🚀 MathPlay іске қосылуда..."
echo "------------------------------------------------"

# 1. Python тексеру
if ! command -v python3 &> /dev/null
then
    echo "❌ Қате: Python3 орнатылмаған. Өтініш, python.org сайтынан орнатыңыз."
    exit
fi

# 2. Виртуалды ортаны тексеру
if [ ! -d "venv" ]; then
    echo "📦 Бірінші рет іске қосылуда. Кітапханалар орнатылуда..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 3. Мәліметтер қорын дайындау
python3 manage.py migrate

# 4. Браузерді ашу
sleep 2 && open "http://127.0.0.1:8000" &

# 5. Серверді бастау
echo "✅ Сайт дайын! Браузер автоматты түрде ашылуы тиіс."
echo "🌍 Жергілікті желідегі мекен-жай: http://$(ipconfig getifaddr en0):8000"
echo "------------------------------------------------"
python3 manage.py runserver 0.0.0.0:8000
