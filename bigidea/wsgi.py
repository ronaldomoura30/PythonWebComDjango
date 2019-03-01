"""
WSGI config for bigidea project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigidea.settings')

from django.core.wsgi import get_wsgi_application

# ------------------  Heroku -----------------------------------
from df_static import Cling

application = Cling(get_wsgi_application())

# ------------------  Versão Antiga ----------------------------
# application = get_wsgi_application()
