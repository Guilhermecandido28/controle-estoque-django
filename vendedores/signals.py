from vendas.models import Vendas
from .models import EventoVenda, Vendedores
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from decimal import Decimal

@receiver(post_save, sender=Vendas)
def cria_evento_venda(sender, instance, created, **kwargs):
    if created:
        try:
            # print("Criando EventoVenda para a venda:", instance)
            # print("Vendedor:", instance.vendedor)
            # print("Descrição:", instance.descricao)
            # print("Total:", instance.total)
            
            EventoVenda.objects.create(
                vendedor=instance.vendedor,
                produto=instance.descricao,
                total=instance.total,
                data=timezone.now()
            )
            print("EventoVenda criado com sucesso!")
        except Exception as e:
            print(f'Erro ao criar EventoVenda: {e}')


@receiver(post_save, sender=Vendas)
def atualizar_produtos_vendidos(sender, instance, **kwargs):
    venda = instance.vendedor    
    try:
        vendedor = Vendedores.objects.get(nome=venda)        
        vendedor.total_em_vendas += instance.total        
        vendedor.comissao += instance.total * Decimal(vendedor.porcentegem_comissao/100)        
        vendedor.save()        
    except Vendedores.DoesNotExist:
        print(f'Vendedor com o nome {venda} não encontrado.')
    except Exception as e:
        print(f'Erro ao atualizar produtos vendidos: {e}')


    