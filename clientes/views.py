from django.shortcuts import render
from .models import Clientes

def clientes(request):
    if request.user.is_authenticated:
        object = Clientes.objects.all()
        objeto_maior_id = Clientes.objects.order_by('id').last()                           
        template = 'clientes/cliente.html'
        context = {'object': object, 'last_cliente': objeto_maior_id}
        return render(request, template, context)
