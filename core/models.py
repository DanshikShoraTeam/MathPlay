import random
import string
from django.db import models
from django.contrib.auth.models import User

# ========== ПРОФИЛЬ СТУДЕНТА ==========
# Расширенный профиль пользователя для отслеживания прогресса в игре
class StudentProfile(models.Model):
    # Связь один-к-одному с пользователем Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Количество набранных очков опыта
    xp = models.IntegerField(default=0)
    # Текущий уровень пользователя
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

# ========== ИГРА ==========
# Модель для хранения информации об игре: вопросы, тип, автор и статистика
class Game(models.Model):
    # Типы доступных игр
    GAME_TYPES = [
        ('froggy', 'Froggy Jumps'),
        ('match', 'Match'),
        ('memory', 'Memory'),
        ('fill_blank', 'Fill in the Blank'),
        ('quiz', 'Quiz'),
    ]
    
    # Название игры
    title = models.CharField(max_length=200)
    # Тип игры из списка выше
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    # Автор/создатель игры
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Вопросы в формате JSON: [{"q": "Вопрос", "a": "Ответ", "wrong": ["неправильный1", "неправильный2"]}]
    questions = models.JSONField(default=list)
    # Дата создания игры
    created_at = models.DateTimeField(auto_now_add=True)
    # Опубликована ли игра (доступна для игроков)
    is_published = models.BooleanField(default=False)
    # Код для публикации (для поделиться с другими)
    publish_code = models.CharField(max_length=10, unique=True, blank=True)
    # Количество раз, которые игра была сыграна
    play_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Если код публикации еще не был сгенерирован - создаем случайный код
        if not self.publish_code:
            self.publish_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# ========== СЕССИЯ ИГРЫ ==========
# Сохраняет результаты каждого сыгранного сеанса игры студентом
class GameSession(models.Model):
    # Ссылка на игру
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    # Имя студента (не обязательно зареги, может быть анонимным игроком)
    student_name = models.CharField(max_length=100)
    # Процент правильных ответов (0-100)
    score_percent = models.IntegerField()
    # Количество полученного опыта за эту игру
    xp_earned = models.IntegerField()
    # Время прохождения в секундах
    time_seconds = models.IntegerField()
    # Когда игра была завершена
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.game.title}"
