import sys

from config.components.environ import env

if 'pytest' in str(sys.argv):
    DATABASES = {'default': env.db('SQLITE_DATABASE_URL')}
else:
    DATABASES = {'default': env.db()}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
