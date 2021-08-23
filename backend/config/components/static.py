from config.components.environ import env, root

STATIC_URL = env.str('STATIC_URL', default='static/')
STATIC_ROOT = root.path('static/')
