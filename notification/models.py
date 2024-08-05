from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=100)
    remetente = models.CharField(max_length=50)
    destinatario = models.CharField(max_length=50)
    data_criacao = models.DateTimeField(auto_now_add=True)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)

    def __str__(self):
        return self.mensagem
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'