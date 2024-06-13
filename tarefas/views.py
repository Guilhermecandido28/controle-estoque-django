from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .forms import TarefasForms
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
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
            # Convertendo os campos inicio e prazo para datetime
            inicio = datetime.strptime(request.POST['inicio'], '%Y-%m-%dT%H:%M')
            prazo = datetime.strptime(request.POST['prazo'], '%Y-%m-%dT%H:%M')
            
            # Salvando o formulário com os dados convertidos
            form = TarefasForms(request.POST)
            if form.is_valid():
                tarefa = form.save(commit=False)
                tarefa.inicio = inicio
                tarefa.prazo = prazo
                tarefa.save()
                messages.success(request, 'A tarefa foi adicionada com sucesso!')
                return render(request, 'partials/_alertas.html')
            
        else:
            # Tratamento de erros
            errors = form.errors.as_data()
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f"Erro no campo '{field}': {error}")
    else:
        form = TarefasForms()
    
    return render(request, 'partials/_alertas.html', {'form': form})

def eventos(request):
    print('chamada a função eventos')
    eventos = Tarefas.objects.all()
    eventos = [{
        'title': evento.tarefa,
        'start': evento.inicio.astimezone(timezone.get_current_timezone()).isoformat(),  # Converta para o fuso horário correto
        'end': evento.prazo.astimezone(timezone.get_current_timezone()).isoformat(),
        'description': (
            f"O funcionário {evento.funcionario.nome} terá que {evento.tarefa} "
            f"no prazo de {evento.inicio.astimezone(timezone.get_current_timezone()).strftime('%d/%m/%Y %H:%M')} "
            f"até {evento.prazo.astimezone(timezone.get_current_timezone()).strftime('%d/%m/%Y %H:%M')}."
        ), 
        'extendedProps': {
            'funcionario': {
                'nome': evento.funcionario.nome,                
            }
        }
    } for evento in eventos]    
    return JsonResponse(eventos, safe=False, encoder=DjangoJSONEncoder)

def marcar_concluida(request):
    print('função marcar concluida chamada')
    data = json.loads(request.body)
    print('passou da importação duvidosa')
    evento_id = data.get('id')

    try:
        evento = get_object_or_404(Tarefas, id=evento_id)
        evento.status = True
        evento.save()
        return JsonResponse({'mensagem': 'Tarefa marcada como concluída'})
    except Tarefas.DoesNotExist:
        return JsonResponse({'erro': 'Tarefa não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
