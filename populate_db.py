import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_platform.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Game

def populate():
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    else:
        admin = User.objects.get(username='admin')

    # Game 1: Алгебра негіздері (Quiz)
    Game.objects.get_or_create(
        title="Алгебра негіздері",
        game_type="quiz",
        author=admin,
        is_published=True,
        questions=[
            {"q": "2x + 4 = 10, x = ?", "a": "3", "wrong": ["2", "4", "5"]},
            {"q": "√144 = ?", "a": "12", "wrong": ["11", "13", "14"]},
            {"q": "3² + 4² = ?", "a": "25", "wrong": ["20", "30", "27"]},
            {"q": "15% от 200 = ?", "a": "30", "wrong": ["25", "35", "20"]},
            {"q": "2³ = ?", "a": "8", "wrong": ["6", "9", "16"]},
            {"q": "(-3)×(-4) = ?", "a": "12", "wrong": ["-12", "7", "-7"]},
            {"q": "Үшбұрыш бұрыштары қосындысы?", "a": "180°", "wrong": ["90°", "360°", "270°"]},
            {"q": "0.5 = ?%", "a": "50%", "wrong": ["5%", "500%", "0.5%"]},
            {"q": "sin 30° = ?", "a": "0.5", "wrong": ["0", "1", "√2/2"]},
            {"q": "cos 0° = ?", "a": "1", "wrong": ["0", "-1", "0.5"]}
        ]
    )

    # Game 2: Көбейту жарысы (Froggy)
    Game.objects.get_or_create(
        title="Көбейту жарысы",
        game_type="froggy",
        author=admin,
        is_published=True,
        questions=[
            {"q": "7 × 8 = ?", "a": "56", "wrong": ["54", "58", "52"]},
            {"q": "9 × 6 = ?", "a": "54", "wrong": ["48", "56", "63"]},
            {"q": "12 × 7 = ?", "a": "84", "wrong": ["82", "86", "74"]},
            {"q": "8 × 8 = ?", "a": "64", "wrong": ["56", "72", "68"]},
            {"q": "11 × 9 = ?", "a": "99", "wrong": ["88", "111", "98"]},
            {"q": "6 × 7 = ?", "a": "42", "wrong": ["36", "48", "40"]},
            {"q": "13 × 4 = ?", "a": "52", "wrong": ["48", "56", "42"]},
            {"q": "9 × 9 = ?", "a": "81", "wrong": ["72", "90", "80"]},
            {"q": "7 × 7 = ?", "a": "49", "wrong": ["42", "56", "48"]},
            {"q": "8 × 6 = ?", "a": "48", "wrong": ["40", "54", "42"]}
        ]
    )

    # Game 3: Формула жұптары (Memory)
    Game.objects.get_or_create(
        title="Формула жұптары",
        game_type="memory",
        author=admin,
        is_published=True,
        questions=[
            {"q": "x²-y²", "a": "(x+y)(x-y)"},
            {"q": "S шеңбері", "a": "πr²"},
            {"q": "sin 30°", "a": "0.5"},
            {"q": "Пифагор", "a": "a²+b²=c²"},
            {"q": "cos 60°", "a": "0.5"},
            {"q": "S үшбұрыш", "a": "½×a×h"},
            {"q": "tan 45°", "a": "1"},
            {"q": "S тіктөртбұрыш", "a": "a×b"}
        ]
    )

    print("Platform populated with updated sample data!")

if __name__ == '__main__':
    populate()
