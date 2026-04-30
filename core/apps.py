from django.apps import AppConfig

# Django-ға "core" деген қосымша бар екенін хабарлайтын файл.
# settings.py-дағы INSTALLED_APPS тізіміне "core" жазылғанда Django осы класты табады.
class CoreConfig(AppConfig):
    name = 'core'
