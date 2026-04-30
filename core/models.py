import random
import string
from django.db import models
from django.contrib.auth.models import User


# --- ПРОФИЛЬ СТУДЕНТА ---
# Расширяет стандартного пользователя Django: добавляет очки опыта и уровень
class StudentProfile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    xp    = models.IntegerField(default=0)   # накопленные очки опыта
    level = models.IntegerField(default=1)   # текущий уровень игрока

    def __str__(self):
        return self.user.username


# --- ИГРА ---
# Хранит одну игру: название, тип, вопросы и статистику запусков
class Game(models.Model):
    GAME_TYPES = [
        ('froggy',     'Froggy Jumps'),
        ('match',      'Match'),
        ('memory',     'Memory'),
        ('fill_blank', 'Fill in the Blank'),
        ('quiz',       'Quiz'),
    ]

    title        = models.CharField(max_length=200)
    game_type    = models.CharField(max_length=20, choices=GAME_TYPES)
    author       = models.ForeignKey(User, on_delete=models.CASCADE)
    # Вопросы хранятся списком словарей: [{"q": "...", "a": "...", "wrong": [...]}]
    questions    = models.JSONField(default=list)
    created_at   = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)   # опубликована ли игра
    publish_code = models.CharField(max_length=10, unique=True, blank=True)  # короткий код для ученика
    play_count   = models.IntegerField(default=0)       # сколько раз сыграли

    def save(self, *args, **kwargs):
        # При первом сохранении генерируем случайный код из 6 символов
        if not self.publish_code:
            self.publish_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=6)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# --- СЕССИЯ ИГРЫ ---
# Записывает результат каждого прохождения игры учеником
class GameSession(models.Model):
    game          = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    student_name  = models.CharField(max_length=100)   # имя ученика (необязательно авторизован)
    score_percent = models.IntegerField()               # процент правильных ответов (0–100)
    xp_earned     = models.IntegerField()               # заработанный опыт за эту игру
    time_seconds  = models.IntegerField()               # время прохождения в секундах
    completed_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.game.title}"
