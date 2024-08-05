
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notification.services import criar_notificacao
from tarefas.models import Tarefas
from vendas.models import Vendas

@receiver(post_save, sender=Tarefas)
def post_created(sender, instance, created, **kwargs):
    if created:
        destinatario = instance.funcionario.nome
        titulo = f"Tarefa para {destinatario}"
        rementente = "Gerencia"
        mensagem = f"{instance.tarefa}, no dia {instance.inicio.strftime("%d/%m/%Y %H:%M:%S")} até {instance.prazo.strftime("%d/%m/%Y %H:%M:%S")}."
        criar_notificacao(titulo=titulo, remetente=rementente, destinatario=destinatario, mensagem=mensagem)
    else:
        if instance.status:
            rementente = "Gerencia"
            titulo = f"Tarefa concluída"
            destinatario = instance.funcionario.nome
            mensagem = f"{instance.tarefa}, concluída por {destinatario}."
            criar_notificacao(titulo=titulo, remetente=rementente, destinatario=destinatario, mensagem=mensagem)
        else:
            destinatario = instance.funcionario.nome
            titulo = f"Tarefa editada para {destinatario}"
            rementente = "Gerencia"
            mensagem = f"{instance.tarefa}, no dia {instance.inicio.strftime("%d/%m/%Y %H:%M:%S")} até {instance.prazo.strftime("%d/%m/%Y %H:%M:%S")}."
            criar_notificacao(titulo=titulo, remetente=rementente, destinatario=destinatario, mensagem=mensagem)

@receiver(post_delete, sender=Tarefas)
def post_tarefa_delete(sender, instance, **kwargs):
    destinatario = instance.funcionario.nome
    titulo = f"Tarefa excluída para {destinatario}"
    remetente = "Gerência"
    mensagem = f"{instance.tarefa} foi excluída."
    criar_notificacao(titulo=titulo, remetente=remetente, destinatario=destinatario, mensagem=mensagem)


@receiver(post_save, sender=Vendas)
def post_created_vendas(sender, instance, created, **kwargs):
    if created:
        destinatario = "Gerencia"
        if instance.cliente == None:
            titulo = 'Venda realizada'
        else:
            titulo = f"Venda realizada para {instance.cliente}"
        rementente = "Gerencia"
        mensagem = f"Vendido no dia {instance.data.strftime("%d/%m/%Y %H:%M:%S")} um total de R${str(instance.total).replace('.',',')}."
        criar_notificacao(titulo=titulo, remetente=rementente, destinatario=destinatario, mensagem=mensagem)
