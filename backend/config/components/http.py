from config.components.environ import env

ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', default='*').split()
