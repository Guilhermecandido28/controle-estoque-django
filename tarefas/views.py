from django.shortcuts import render

def tarefas(request):
    return render(request, 'tarefas/tarefas.html')
