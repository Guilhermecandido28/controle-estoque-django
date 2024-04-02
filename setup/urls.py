from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('', include('login.urls')),
    path('estoque/', include('estoque.urls')),
    path('clientes/', include('clientes.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
