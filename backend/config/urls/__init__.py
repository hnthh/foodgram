from django.conf.urls import include
from django.contrib import admin
from django.urls import path

api = [
    path('', include('config.urls.v2')),
]

urlpatterns = [
    path('api/', include(api)),
    path('admin/', admin.site.urls),
]
