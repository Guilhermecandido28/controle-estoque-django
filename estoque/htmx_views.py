from .models import Estoque, CategoriaEstoque, MarcaEstoque
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import FileResponse
from .forms import EditarForm, AddEstoqueForms, AddCategoriaForm, AddMarcaForm
from .filters import EstoqueFilter
from django.db.models import F
from django.contrib import messages
from django.http import JsonResponse
from custom_tags import custom_filters
from .functions import criar_etiqueta





def salvar_produtos(request):
    form = AddEstoqueForms(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return render(request, 'estoque/partials/_linha_tabela.html', {'object': obj})
        else:
            # Se o formulário não for válido, retorne uma resposta JSON com os erros
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)


@csrf_exempt
@require_http_methods(['DELETE'])
def deletar_produtos(request, id):
    template_name = 'estoque/partials/_table.html'
    obj = Estoque.objects.get(codigo_barras=id)
    obj.delete()    
    return render(request, template_name)


def imprimir_produto(request, id): 
    obj = Estoque.objects.get(codigo_barras=id)
    pdf_file = criar_etiqueta(obj.codigo_barras, custom_filters.currency(obj.venda), obj.tamanho)
    
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="etiqueta.pdf"'
    
    return response
    


def editar_produto(request, id):
    template_name = 'estoque/partials/estoque_forms.html'
    obj = Estoque.objects.get(codigo_barras=id)
    print('Instância:', obj)
    print('Categoria:', type(obj.categoria))
    print('Marca:', type(obj.marca))
    
    form = EditarForm(request.POST or None, instance=obj)    

    
    context = {'object': obj, 'form': form}

    return render(request, template_name, context)


def update_produto(request, id):
    template_name = 'estoque/partials/_linha_tabela.html'    
    obj = Estoque.objects.get(codigo_barras=id)
    form = EditarForm(request.POST or None, instance=obj)    
    context = {'object': obj}
    if request.method == 'POST':        
        if form.is_valid():            
            form.save()            
        else:
            errors = form.errors.as_data()
            context['errors'] = errors
            print('Erro:', errors)
    return render(request, template_name, context)


def pesquisar_produtos(request):
    # Obter os dados do formulário de pesquisa
    filtro = EstoqueFilter(request.POST, queryset=Estoque.objects.all())
    
    # Aplicar o filtro
    obj = filtro.qs

    template_name = 'estoque/partials/_table.html'    
    context = {'object': obj, 'filtro': filtro}        
    return render(request, template_name, context)

def estoque_baixo(request):
    obj = Estoque.objects.filter(quantidade__lte=F('estoque_minimo')) 
    template_name = 'estoque/partials/_table.html' 
    context = {'object': obj}
    return render(request, template_name, context)


def add_categoria(request):
    template_name = 'estoque/partials/addcategoria_forms.html'   
    form = AddCategoriaForm()
    context = {'form': form}
    return render(request, template_name, context)


def update_categoria(request):
    form_cat = AddCategoriaForm(request.POST or None)
    form = AddEstoqueForms()
    context = {'form': form}
    if request.method == 'POST':
        if form_cat.is_valid():
            form_cat.save()   
            messages.success(request, f'Categoria {request.POST.get('categoria')} adicionado(a)!')
        elif not request.POST.get('categoria').strip():
            messages.error(request, 'Campo categoria não pode ser vazio!')
        else:
            messages.error(request, f"A Categoria {request.POST.get('categoria')} já existe.")
    return render(request, 'estoque/partials/_campo_categoria.html', context)


def deletar_categoria(request):
    valor = request.POST.get('categoria')    
    template_name = 'estoque/partials/_campo_categoria.html'
    form = AddEstoqueForms()
    context = {'form': form}
    try:
        obj = CategoriaEstoque.objects.get(categoria=valor)
        obj.delete()
        messages.success(request, f'Categoria {request.POST.get('categoria')} deletado(a)!')
    except:
        messages.error(request, f'Categoria {valor} não encontrado(a)!')    
    return render(request, template_name, context)    
    

def add_marca(request):
    template_name = 'estoque/partials/addmarca_forms.html'   
    form = AddMarcaForm()
    context = {'form': form}
    return render(request, template_name, context)


def update_marca(request):
    form_cat = AddMarcaForm(request.POST or None)
    form = AddEstoqueForms()
    context = {'form': form}
    if request.method == 'POST':
        if form_cat.is_valid():
            form_cat.save()   
            messages.success(request, f'Marca {request.POST.get('marca')} adicionado(a)!')
        elif not request.POST.get('marca').strip():
            messages.error(request, 'Campo marca não pode ser vazio!')            
        else:
            messages.error(request, f"A Marca {request.POST.get('marca')} já existe.")
    return render(request, 'estoque/partials/_campo_marca.html', context)


def deletar_marca(request):
    valor = request.POST.get('marca')    
    template_name = 'estoque/partials/_campo_marca.html'
    form = AddEstoqueForms()
    context = {'form': form}    
    try:
        obj = MarcaEstoque.objects.get(marca=valor)
        obj.delete()
        messages.success(request, f'Marca {request.POST.get('marca')} deletado(a)!')
    except:
        messages.error(request, f'Marca {valor} não encontrado(a)!')    
    return render(request, template_name, context)


