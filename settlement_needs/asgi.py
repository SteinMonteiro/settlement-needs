"""
ASGI config for settlement_needs project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settlement_needs.settings')

application = get_asgi_application()
