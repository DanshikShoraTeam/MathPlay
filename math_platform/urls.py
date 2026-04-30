from django.contrib import admin
from django.urls import path, include

# Корневые URL проекта: панель администратора и все URL приложения core
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
