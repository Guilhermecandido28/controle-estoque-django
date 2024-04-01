from django.shortcuts import render,redirect
from django.contrib import messages

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home/index.html')
    else:
        messages.error(request, 'Faça o login para acessar o sistema.')
        return redirect('login')
