from django.urls import path
from . import views, services

urlpatterns = [
    path('marcar_notificacao_lida/<int:notification_id>/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('marcar_todas_lida/', views.marcar_todas_como_lida, name='marcar_todas_como_lida'),
     path('load-more-notifications/', services.load_more_notifications, name='load_more_notifications'),
    
]