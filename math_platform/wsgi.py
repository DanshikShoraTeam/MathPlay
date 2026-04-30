import os
from django.core.wsgi import get_wsgi_application

# WSGI — веб-сервер мен Django арасындағы байланыс протоколы.
# Хостингке шығарғанда (Gunicorn, Apache, Nginx) осы файл арқылы жұмыс істейді.
# Жергілікті жұмыста (runserver) бұл файл пайдаланылмайды.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_platform.settings')
application = get_wsgi_application()
