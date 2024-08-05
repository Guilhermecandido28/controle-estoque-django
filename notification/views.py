
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notification






def marcar_notificacao_lida(request, notification_id):
    if request.method == 'GET':
        notification = get_object_or_404(Notification, pk=notification_id)
        notification.lida = True
        notification.save()
        return JsonResponse({'message': 'Notificação marcada como lida.'}, status=200)
    return JsonResponse({'error': 'Erro ao processar a requisição.'}, status=400)

def marcar_todas_como_lida(request):
    if request.method == 'GET':
        notifications = Notification.objects.all()
        for notification in notifications:
            notification.lida = True
            notification.save()
        return JsonResponse({'message': 'Todas as notificações marcadas como lidas.'})
    return JsonResponse({'error': 'Erro ao processar a requisição.'}, status=400)

