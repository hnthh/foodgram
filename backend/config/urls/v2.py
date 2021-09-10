from django.urls import include, path

urlpatterns = [
    path('ingredients/', include('ingredients.urls')),
    path('recipes/', include('recipes.urls')),
    path('tags/', include('tags.urls')),
    path('users/', include('users.urls')),

    path('auth/', include('djoser.urls.authtoken')),
]
