import os
import sys
# python
sys.path.append('/data2/python_venv/2.7/djtinue/lib/python2.7/')
sys.path.append('/data2/python_venv/2.7/djtinue/lib/python2.7/site-packages/')
sys.path.append('/data2/python_venv/2.7/djtinue/lib/django_projects/')
sys.path.append('/data2/python_venv/2.7/djtinue/lib/django-djtinue/')
# django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djtinue.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/var/cache/python/.python-eggs")
os.environ.setdefault("TZ", "America/Chicago")
# wsgi
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
