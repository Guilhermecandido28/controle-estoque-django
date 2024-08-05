from django.urls import path
from . import views
from . import utils



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('card1_saidas/', views.card1_saidas, name='card1_saidas'),
    path('card1_entradas/', views.card1_entradas, name='card1_entradas'),
    path('card2_saidas/', views.card2_saidas, name='card2_saidas'),
    path('card2_entradas/', views.card2_entradas, name='card2_entradas'),
    path('card3_saidas/', views.card3_saidas, name='card3_saidas'),
    path('card3_entradas/', views.card3_entradas, name='card3_entradas'),
    path('card4_saidas/', views.card4_saidas, name='card4_saidas'),
    path('card4_entradas/', views.card4_entradas, name='card4_entradas'),
    path('card5_saidas/', views.card5_saidas, name='card5_saidas'),
    path('card5_entradas/', views.card5_entradas, name='card5_entradas'),
    path('vendasxmes/', utils.Graficos.vendasxmes, name='vendasxmes'),    
    path('vendasxdia/', utils.Graficos.vendasxdia, name='vendasxdia'),
    path('vendasxfp_mes/', utils.Graficos.vendasxfp_mes, name='vendasxfp_mes'),
    path('vendasxfp_dia/', utils.Graficos.vendasxfp_dia, name='vendasxfp_dia'),
    path('salvar_saida/', views.salvar_saida, name='salvar_saida'),
]