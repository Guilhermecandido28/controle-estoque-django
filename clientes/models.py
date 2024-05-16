from django.db import models
from .functions import obter_url_foto_perfil

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=250)
    telefone = models.CharField(max_length=15, default='Não Possui')
    email = models.EmailField(max_length=50, default='NPossui@email.com')
    instagram = models.CharField(max_length=50, default='Não Possui')
    url_instagram = models.URLField(blank=True, default="https://xsgames.co/randomusers/avatar.php?g=pixel")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Clientes'


    def save(self, *args, **kwargs):
            urls_padrao = [
                 "https://xsgames.co/randomusers/avatar.php?g=pixel"
            ]
            if self.instagram != 'Não Possui':
                self.url_instagram = obter_url_foto_perfil(self.instagram)
            else:
                self.url_instagram = urls_padrao[0]
            super(Clientes, self).save(*args, **kwargs)

class Eventos(models.Model):
     cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
     titulo = models.CharField(max_length=250)
     data_evento = models.DateTimeField()

     class Meta:
        verbose_name_plural = 'Eventos'
