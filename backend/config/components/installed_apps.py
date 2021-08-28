INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'coverage',
    'django_filters',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'djoser',

    'ingredients.apps.IngredientsConfig',
    'recipes.apps.RecipesConfig',
    'tags.apps.TagsConfig',
    'users.apps.UsersConfig',
]
