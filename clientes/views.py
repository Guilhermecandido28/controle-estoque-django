from django.shortcuts import render
from .models import Clientes, Eventos
from django.http import JsonResponse
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

def clientes(request):
    if request.user.is_authenticated:
        object = Clientes.objects.all()
        objeto_maior_id = Clientes.objects.order_by('id').last()                           
        template = 'clientes/cliente.html'
        context = {'object': object, 'last_cliente': objeto_maior_id}
        return render(request, template, context)


def eventos_calendario(request):
    eventos = Eventos.objects.all().values('titulo', 'data_evento')
    eventos = [{
        'title': evento['titulo'],
        'start': timezone.localtime(evento['data_evento']).strftime('%Y-%m-%d %H:%M:%S')        
    } for evento in eventos]    
    return JsonResponse(list(eventos), safe=False, encoder=DjangoJSONEncoder)