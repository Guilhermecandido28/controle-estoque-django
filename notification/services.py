from .models import Notification
from django.utils import timezone
from django.http import JsonResponse


def criar_notificacao(titulo, remetente, destinatario, mensagem):
    excluir_notificacoes_antigas()
    notificacao = Notification.objects.create(
        title=titulo,
        remetente=remetente,
        destinatario=destinatario,
        mensagem=mensagem,
        )
    notificacao.save()
    return notificacao

def contagem_notificacao_n_lidas(request):
    contagem = Notification.objects.filter(lida=False).count()
    return {'contagem': contagem}

def notificacao_unread(request):
    unread_notifications = Notification.objects.filter(lida=False).all()    
    return {'unread_notifications': unread_notifications}

def notificacao_read(request):
    read_notifications = Notification.objects.filter(lida=True).all()
    return {'read_notifications': read_notifications}

def excluir_notificacoes_antigas():
    limite_tempo = timezone.now() - timezone.timedelta(days=30)
    Notification.objects.filter(data_criacao__lte=limite_tempo).delete()

def load_more_notifications(request):
    offset = int(request.GET.get('offset', 0))
    limit = 10
    notifications = Notification.objects.filter(is_read=False)[offset:offset + limit]
    data = {
        'notifications': list(notifications.values('id', 'title', 'mensagem', 'data_criacao'))
    }
    return JsonResponse(data)