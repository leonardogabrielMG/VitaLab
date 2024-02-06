from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        
        primeiro_nome = request.POST.get("primeiro_nome")
        ultimo_nome = request.POST.get("ultimo_nome")
        username = request.POST.get("username")
        senha = request.POST.get("senha")
        email = request.POST.get("email")
        confirmar_senha = request.POST.get("confirmar_senha")
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, "As senhas não são iguais!")
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, "A senha deve possuir no mínimo 6 caracteres!")
            return redirect('/usuarios/cadastro')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, "Usuário já existe!")
            return redirect('/usuarios/cadastro')
        
        try:
            user = User.objects.create_user(
                first_name = primeiro_nome,
                last_name = ultimo_nome,
                username=username,
                email=email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso!")
            return redirect('/usuarios/logar/')
        except:
            messages.add_message(request, constants.ERROR, "Erro interno do sistema!")
            return redirect('/usuarios/cadastro')
        
        
        return

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)
        
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, "Logado com sucesso!")
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, "Usuário ou senha incorreto!")
            return redirect('/usuarios/logar/')
