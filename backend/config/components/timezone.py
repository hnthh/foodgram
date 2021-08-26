from config.components.environ import env

USE_TZ = False

TIME_ZONE = env.str('TIME_ZONE', default='Europe/Moscow')
