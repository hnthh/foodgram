from split_settings.tools import include

from config.components.environ import env, root

SITE_ROOT = root()

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

include(
    'components/api.py',
    'components/auth.py',
    'components/boilerplate.py',
    'components/db.py',
    'components/http.py',
    'components/i18n.py',
    'components/installed_apps.py',
    'components/media.py',
    'components/middleware.py',
    'components/static.py',
    'components/templates.py',
    'components/timezone.py',
)
