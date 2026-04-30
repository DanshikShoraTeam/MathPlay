from django.contrib import admin
from .models import Game, GameSession, StudentProfile

# Регистрация моделей в панели администратора Django (/admin/)
# После регистрации можно просматривать и редактировать данные через браузер
admin.site.register(Game)
admin.site.register(GameSession)
admin.site.register(StudentProfile)
