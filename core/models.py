import random
import string
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

class Game(models.Model):
    GAME_TYPES = [
        ('froggy', 'Froggy Jumps'),
        ('match', 'Match'),
        ('memory', 'Memory'),
        ('fill_blank', 'Fill in the Blank'),
        ('quiz', 'Quiz'),
    ]
    
    title = models.CharField(max_length=200)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.JSONField(default=list)  # List of {q: "", a: "", wrong: []}
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    publish_code = models.CharField(max_length=10, unique=True, blank=True)
    play_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.publish_code:
            self.publish_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class GameSession(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    student_name = models.CharField(max_length=100)
    score_percent = models.IntegerField()
    xp_earned = models.IntegerField()
    time_seconds = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.game.title}"
