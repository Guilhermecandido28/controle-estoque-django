from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .forms import TarefasForms
from .filters import TarefasFilter
from django.contrib import messages
from django.utils import timezone
from .models import Tarefas
from django.core.serializers.json import DjangoJSONEncoder


def tarefas(request):
    forms = TarefasForms()    
    template_name = 'tarefas/tarefas.html'
    context = {'forms': forms}
    return render(request, template_name, context)

def adicionar_tarefa(request):    
    if request.method == 'POST':
        
        form = TarefasForms(request.POST)
        if form.is_valid():
            
            tarefa = form.save()
            
            
            # Retornar dados da tarefa para atualização do FullCalendar
            return JsonResponse({
                'success': True,
                'id': tarefa.id,
                'tarefa': tarefa.tarefa,
                'inicio': tarefa.inicio.isoformat(),
                'prazo': tarefa.prazo.isoformat(),
                'responsavel': tarefa.funcionario.nome,
                'status': tarefa.status,
                'color' : tarefa.cor,
            })

        else:
            
            errors = []
            for field, field_errors in form.errors.as_data().items():
                for error in field_errors:
                    errors.append(f"Erro no campo '{field}': {error}")
            return JsonResponse({'success': False, 'errors': errors})
    else:
        
        return JsonResponse({'success': False, 'errors': ['Método não permitido']})

def eventos(request):
    print('chamada a função eventos')
    eventos = Tarefas.objects.all()
    eventos = [{
        'title': evento.tarefa,
        'start': evento.inicio.astimezone(timezone.get_current_timezone()).isoformat(),  # Converta para o fuso horário correto
        'end': evento.prazo.astimezone(timezone.get_current_timezone()).isoformat(),
        'id': evento.id,
        'color' : evento.cor,        
        'extendedProps': {
            'funcionario': {
                'nome': evento.funcionario.nome,                
            },
            'status': evento.status
        }
    } for evento in eventos]    
    return JsonResponse(eventos, safe=False, encoder=DjangoJSONEncoder)

def editar_tarefa(request, pk):
    editar_tarefa = get_object_or_404(Tarefas, pk=pk)
    if request.method == 'POST':
        form = TarefasForms(request.POST, instance=editar_tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, 'A tarefa foi adicionada com sucesso!')
            return render(request, 'partials/_alertas.html')
    else:
        form = TarefasForms(instance=editar_tarefa)
    return render(request, 'tarefas/partials/editar_tarefa.html', {'forms': form})


