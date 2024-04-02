from . import views
from django.urls import path


urlpatterns = [
    path('', views.clientes, name='clientes'),
    
    ] 