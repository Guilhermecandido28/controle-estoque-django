from vendas.models import Vendas
from .models import EventoVenda
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

@receiver(post_save, sender=Vendas)
def cria_evento_venda(sender, instance, created, **kwargs):
    if created:
        try:
            print("Criando EventoVenda para a venda:", instance)
            print("Vendedor:", instance.vendedor)
            print("Descrição:", instance.descricao)
            print("Total:", instance.total)
            
            EventoVenda.objects.create(
                vendedor=instance.vendedor,
                produto=instance.descricao,
                total=instance.total,
                data=timezone.now()
            )
            print("EventoVenda criado com sucesso!")
        except Exception as e:
            print(f'Erro ao criar EventoVenda: {e}')