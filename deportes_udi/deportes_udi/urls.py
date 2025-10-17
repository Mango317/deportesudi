from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eventos.urls')),

    #  Incluye las rutas de autenticación de Django (esto es clave)
    path('accounts/', include('django.contrib.auth.urls')),
]
