from django.shortcuts import render, redirect
from login.forms import LoginForms, CadastroForms
from django.contrib.auth.models import  User
from django.contrib import auth
from django.contrib import messages
from rolepermissions.roles import assign_role

def login(request):
    if not request.user.is_authenticated:
        form = LoginForms()
        if request.method == 'POST':
            form = LoginForms(request.POST)
            if form.is_valid():
                nome = form['nome_login'].value()
                senha = form['senha'].value()

            usuario = auth.authenticate(
                request,
                username = nome,
                password = senha
            )
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f'{nome.title()}, seu login foi realizado com sucesso!')
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou Senha inválido(s)! Tente novamente.')
                return redirect('login')
        return render(request, 'login/login.html', {"form": form})
    else:
        return redirect('home')

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)        
        if form.is_valid():           
            
            nome = form["nome_cadastro"].value()
            email = form["email"].value()
            senha = form["senha_1"].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existe.')
                return redirect('cadastro')

            usuario = User.objects.create_user(
                username=nome,
                password=senha,
                email=email
            )

            usuario.save()
            assign_role(usuario, 'vendedor')
            messages.success(request, f'Cadastrado com Sucesso!, {nome}. Agora você pode fazer o Login!')
            return redirect('login')

    return render(request, 'login/cadastro.html', {"form": form})
    
def logout(request):    
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')