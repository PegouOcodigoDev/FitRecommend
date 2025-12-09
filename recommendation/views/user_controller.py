from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..repositories import UserRepository
from ..forms import UserForm


@login_required
def user_profile(request):
    """Exibe perfil completo do usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do template user_profile.html ou redirecionamento
        para configuração de perfil se não existir.
    """
    user_repository = UserRepository()
    
    try:
        app_user = user_repository.get_by_email(request.user.email)
        if not app_user:
            return redirect('recommendation:profile_setup')
    except:
        return redirect('recommendation:profile_setup')
    
    return render(request, 'recommendation/user_profile.html', {
        'user': app_user,
        'has_preferences': hasattr(app_user, 'preferencias')
    })


@login_required
def user_setup(request):
    """Configura perfil inicial do usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do formulário de configuração ou redirecionamento
        após salvamento bem-sucedido.
    """
    user_repository = UserRepository()
    
    try:
        existing_user = user_repository.get_by_email(request.user.email)
        if existing_user:
            return redirect('recommendation:profile')
    except:
        pass
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            app_user = form.save(commit=False)
            app_user.email = request.user.email
            app_user.nome = request.user.username
            app_user.save()
            messages.success(request, 'Perfil configurado com sucesso!')
            return redirect('recommendation:home')
    else:
        initial_data = {
            'nome': request.user.username,
            'email': request.user.email
        }
        form = UserForm(initial=initial_data)
    
    return render(request, 'recommendation/user_form.html', {
        'form': form,
        'title': 'Configurar Perfil',
        'button_text': 'Salvar'
    })


@login_required
def user_edit(request):
    """Edita perfil do usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do formulário de edição ou redirecionamento
        após atualização bem-sucedida.
    """
    user_repository = UserRepository()
    app_user = user_repository.get_by_email(request.user.email)
    
    if not app_user:
        return redirect('recommendation:profile_setup')
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=app_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('recommendation:profile')
    else:
        form = UserForm(instance=app_user)
    
    return render(request, 'recommendation/user_form.html', {
        'form': form,
        'title': 'Editar Perfil',
        'button_text': 'Salvar'
    })
