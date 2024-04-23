from django.db.models.signals import post_save
from django.utils import timezone
import pytz
from clientes.models import Eventos, Clientes


def cria_evento(sender, instance, created, **kwargs):
     data_hora = timezone.now().astimezone(pytz.timezone('America/Sao_paulo'))
     if created:
        Eventos.objects.create(
            cliente=instance,
            titulo=f"{instance.nome} Cadastrado!",
            data_evento=data_hora
        )
post_save.connect(cria_evento, sender=Clientes)