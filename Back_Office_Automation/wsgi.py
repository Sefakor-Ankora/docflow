"""
WSGI config for Back_Office_Automation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.urls import include, path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Back_Office_Automation.settings')

application = get_wsgi_application()



urlpatterns = [
    # Other URL patterns
    path('docflow/', include('docflow.urls')),
]

