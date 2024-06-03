from django.shortcuts import render, HttpResponse
from .forms import ClienteForms
from .models import Clientes

from django.http import JsonResponse



def addcliente(request):
    template = 'clientes/partials/_addcliente.html'
    objeto_maior_id = Clientes.objects.order_by('id').last()
    if request.method == 'POST':
        form = ClienteForms()
        context = {'form': form,'last_cliente': objeto_maior_id}
    return render(request, template, context)
    

def update_cliente(request):
    template = 'clientes/partials/_linha_tabela.html'
    form = ClienteForms(request.POST or None)               
    if request.method == 'POST':        
        if form.is_valid():            
            form.save()
            object = Clientes.objects.order_by('id').last()
            context = {'object': object}
            return render(request,template, context) 
        else:
            # Se o formulário não for válido, retorne uma resposta JSON com os erros
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
            
def ultimo_cliente(request, id=None):    
    template = 'clientes/partials/_last_client.html'
    object = Clientes.objects.order_by('id').last()    
    context = {'last_cliente': object}
    return render(request, template, context)

def ver_cliente(request, id):
    template = 'clientes/partials/_last_client.html'
    object = Clientes.objects.get(id=id)    
    context = {'last_cliente': object}
    return render(request, template, context)
    

def deletar_cliente(request, id):
    template_name = 'clientes/partials/_table.html'
    object = Clientes.objects.get(id=id)
    object.delete()           
    return render(request, template_name)

def editar_cliente(request, id):
    template_name = 'clientes/partials/_editar_cliente.html'
    object = Clientes.objects.get(id=id)
    form = ClienteForms(request.POST or None, instance=object)
    context = {'object': object, 'form': form}
    return render(request, template_name, context)

def update_edicao(request, id):
    template_name = 'clientes/partials/_table.html'
    object = Clientes.objects.get(id=id)
    form = ClienteForms(request.POST or None, instance= object)      
    if request.method == 'POST':       
        if form.is_valid():            
            form.save()
            object = Clientes.objects.all()
            context = {'object': object} 
    return render(request, template_name, context)

def pesquisar_cliente(request):
    template_name = 'clientes/partials/_pesquisar_cliente.html'
    pesquisa = request.POST.get('search')
    object = Clientes.objects.filter(nome__icontains=pesquisa)
    print(object)
    context = {'object': object}
    return render(request, template_name, context)
    







        