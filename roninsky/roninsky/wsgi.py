"""
WSGI config for roninsky project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

profile = os.environ.get('RONINSKY_PROFILE', 'develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roninsky.settings.%s" % profile)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "roninsky.settings")

application = get_wsgi_application()
