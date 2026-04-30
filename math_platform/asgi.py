import os
from django.core.asgi import get_asgi_application

# ASGI — WSGI-нің жаңа нұсқасы, нақты уақытта жұмыс істейтін қосымшалар үшін.
# Бұл жобада пайдаланылмайды — болашақта хостингке шығарғанда қажет болуы мүмкін.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_platform.settings')
application = get_asgi_application()
