from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from .models import Vendedores, EventoVenda
from .filters import VendedorFilter

def vendedores(request):
    obj = Vendedores.objects.last()
    obj_filter = Vendedores.objects.all()
    filter = VendedorFilter(request.GET, queryset=obj_filter)
    template_name = 'vendedores/vendedores.html'
    context = {'obj': obj, 'filter': filter}
    return render(request, template_name, context)

def ver_vendedor(request):   
    filtro = VendedorFilter(request.POST, queryset=Vendedores.objects.all())
    
    
    obj = filtro.qs.first()
    
    if not obj:
        
        return render(request, 'vendedores/partials/ver_vendedor.html', {'error': 'Nenhum vendedor encontrado'})   
    
    
    template_name = 'vendedores/partials/ver_vendedor.html'    
    context = {'obj': obj}        
    return render(request, template_name, context)


def eventos_venda_calendario(request):
    eventos = EventoVenda.objects.all()
    eventos = [{
        'title':f"{evento.vendedor} vendeu {evento.total} reais.",
        'start': timezone.localtime(evento.data).strftime('%Y-%m-%d %H:%M:%S')        
    } for evento in eventos]    
    return JsonResponse(list(eventos), safe=False, encoder=DjangoJSONEncoder)
