from django.shortcuts import render, get_object_or_404, HttpResponse
from notifications.signals import notify
from django.http import JsonResponse, HttpResponseBadRequest
from .forms import TarefasForms
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

def editar_tarefa(request, id):    
    editar_tarefa = get_object_or_404(Tarefas, id=id)
    
    if request.method == 'POST':
        form = TarefasForms(request.POST, instance=editar_tarefa)
        
        if form.is_valid():
            tarefa = form.save()


            # Acessar os campos do objeto salvo
            tarefa_salva = form.instance
        
            return JsonResponse({
                'success': True,
                'id': tarefa_salva.id,
                'tarefa': tarefa_salva.tarefa,
                'start': tarefa_salva.inicio.isoformat(),
                'end': tarefa_salva.prazo.isoformat(),
                'responsavel': tarefa_salva.funcionario.nome,
                'status': tarefa_salva.status,
                'color': tarefa_salva.cor,
            })
        else:
            errors = []
            for field, field_errors in form.errors.as_data().items():
                for error in field_errors:
                    errors.append(f"Erro no campo '{field}': {error}")
            return JsonResponse({'success': False, 'errors': errors})
    else:
        return JsonResponse({'success': False, 'errors': ['Método não permitido']})
    

def apagar_tarefa(request, id):
    if request.method == 'GET':
        tarefa = get_object_or_404(Tarefas, id=id)
        tarefa.delete() 
        
        return JsonResponse({'success': True})
    else:
        errors = []            
        for error in errors:
            errors.append(f"Erro no campo '{errors}': {error}")
    return JsonResponse({'success': False, 'errors': errors})
    

def ver_notificacao(request):
    print('ver_notificação')
    return HttpResponse('fndsifo')




    


