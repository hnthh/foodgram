from config.components.environ import env, root

MEDIA_URL = env.str('MEDIA_URL', default='media/')
MEDIA_ROOT = root.path('media/')
