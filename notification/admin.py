

from django.contrib import admin
from .models import Notification

class Notifications(admin.ModelAdmin):
    list_display = ('id', 'mensagem', 'lida')
    list_display_links = ['id', 'mensagem']
    search_fields = ['id', 'mensagem', 'lida']
    list_per_page = 20
    verbose_name_plural = 'Notificações'

admin.site.register(Notification, Notifications)
