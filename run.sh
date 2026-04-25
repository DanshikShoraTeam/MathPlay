#!/bin/bash
echo "MathPlay сервері іске қосылуда..."
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
