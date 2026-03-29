from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CadastroMoradorForm

def login_view(request):
    if request.method == 'POST':
        # Pega os dados que o usuário digitou no HTML
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # O Django verifica no banco de dados se esse email e senha existem
        user = authenticate(request, email=email, password=senha)

        if user is not None:
            # Regra de Negócio: Verifica o Status da Conta
            if user.statusConta == 'Pendente':
                messages.warning(request, 'Sua conta ainda está aguardando aprovação do Síndico.')
                return redirect('login')
            
            elif user.statusConta == 'Negado':
                messages.error(request, 'Seu cadastro foi negado. Procure a administração.')
                return redirect('login')
            
            else:
                # Se for 'Aprovado', faz o login oficial no sistema!
                login(request, user)
                
                # Roteamento Inteligente: Descobre qual é o tipo de usuário logado
                if hasattr(user, 'sindico'):
                    return redirect('home_sindico')
                elif hasattr(user, 'administrador'):
                    return redirect('home_admin')
                else:
                    return redirect('home_morador')
        else:
            messages.error(request, 'Email ou senha incorretos.')

    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroMoradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Aguarde a aprovação.')
            return redirect('login')
    else:
        form = CadastroMoradorForm()

    return render(request, 'login.html', {'form': form})

# Views apenas para renderizar os painéis (Vamos proteger elas nas próximas sprints)
def home_morador(request):
    return render(request, 'home_morador.html')

def home_admin(request):
    return render(request, 'home_admin.html')

def home_sindico(request):
    return render(request, 'home_sindico.html')

def logout_view(request):
    logout(request)
    return redirect('login')