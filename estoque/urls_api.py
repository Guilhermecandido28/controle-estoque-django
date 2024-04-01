from django.urls import path,include
from estoque.views_api import EstoquesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api_estoque', EstoquesViewSet, basename= 'Estoques')

urlpatterns = [
    #path para acessar as views da API de estoques
    path('', include(router.urls)),  
]