from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.Form):
    """Formulário de registro de novos usuários.
    
    Valida username único, email único e confirmação de senha.
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem')
        
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado')
        return email


class LoginForm(forms.Form):
    """Formulário de login de usuários existentes."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )


def register_view(request):
    """Processa registro de novos usuários.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do formulário de registro ou redirecionamento
        após criação bem-sucedida da conta.
    """
    if request.user.is_authenticated:
        return redirect('recommendation:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Complete seu perfil.')
            return redirect('recommendation:profile_setup')
    else:
        form = RegisterForm()
    
    return render(request, 'recommendation/auth/register.html', {'form': form})


def login_view(request):
    """Processa login de usuários existentes.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do formulário de login ou redirecionamento
        após autenticação bem-sucedida.
    """
    if request.user.is_authenticated:
        return redirect('recommendation:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.username}!')
                return redirect('recommendation:home')
            else:
                messages.error(request, 'Usuário ou senha incorretos')
    else:
        form = LoginForm()
    
    return render(request, 'recommendation/auth/login.html', {'form': form})


@login_required
def logout_view(request):
    """Realiza logout do usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Redirecionamento para página de login.
    """
    logout(request)
    messages.success(request, 'Você saiu da sua conta')
    return redirect('recommendation:login')


@login_required
def delete_account_view(request):
    """Exclui conta do usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização da página de confirmação ou redirecionamento
        após exclusão bem-sucedida da conta.
    """
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso')
        return redirect('recommendation:login')
    
    return render(request, 'recommendation/auth/delete_account.html')

