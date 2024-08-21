from vendas.models import Vendas
from estoque.models import Estoque
from .models import EventoVenda
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import F

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
    venda = instance
    
    produtos_info = venda.descricao 

    for produto_info in produtos_info.split(';'):
        produto_info = produto_info.strip()
        if produto_info:
            partes = produto_info.split(', ')
            if len(partes) != 5:
                print(f"Formato incorreto para: {produto_info}")
                continue
            
            codigo_barras, descricao, tamanho, cor, quantidade = partes
            quantidade = int(quantidade)
            
            # Atualiza o estoque
            try:
                estoque_item = Estoque.objects.get(codigo_barras=codigo_barras, tamanho=tamanho, cor=cor)
                estoque_item.quantidade = F('quantidade') - quantidade
                estoque_item.save()
            except Estoque.DoesNotExist:
                print(f"Item de estoque não encontrado: {codigo_barras}, {descricao}, {tamanho}, {cor}")
    
    print("Estoque atualizado com sucesso.")

    