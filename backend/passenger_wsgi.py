"""
Passenger WSGI entry point for cPanel "Setup Python App".

cPanel'da Python App yaratganda 'Application startup file' ni
shu faylga ko'rsating: passenger_wsgi.py
'Application Entry Point' = application
"""
import os
import sys

# Loyiha papkasini Python path'iga qo'shamiz
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Django settings'ni ko'rsatamiz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dgd_backend.settings')

# WSGI application
from dgd_backend.wsgi import application  # noqa: E402, F401
