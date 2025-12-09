from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..repositories import UserRepository
from ..models import Preferences
from ..forms import PreferencesForm


@login_required
def preferences_create(request):
    """Cria preferências de treino para o usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do formulário de criação ou redirecionamento
        se preferências já existirem.
    """
    user_repository = UserRepository()
    user = user_repository.get_by_email(request.user.email)
    
    if not user:
        return redirect('recommendation:profile_setup')
    
    if hasattr(user, 'preferencias'):
        messages.warning(request, 'Você já possui preferências. Edite-as ao invés de criar novas.')
        return redirect('recommendation:preferences_edit')
    
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            preferences = form.save(commit=False)
            preferences.usuario = user
            preferences.save()
            messages.success(request, 'Preferências criadas com sucesso!')
            return redirect('recommendation:profile')
    else:
        form = PreferencesForm()
    
    return render(request, 'recommendation/preferences_form.html', {
        'form': form,
        'user': user,
        'title': 'Criar Preferências',
        'button_text': 'Criar'
    })


@login_required
def preferences_edit(request):
    """Edita preferências de treino do usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do formulário de edição ou redirecionamento
        se preferências não existirem.
    """
    user_repository = UserRepository()
    user = user_repository.get_by_email(request.user.email)
    
    if not user:
        return redirect('recommendation:profile_setup')
    
    if not hasattr(user, 'preferencias'):
        messages.warning(request, 'Você não possui preferências. Crie-as primeiro.')
        return redirect('recommendation:preferences_create')
    
    if request.method == 'POST':
        form = PreferencesForm(request.POST, instance=user.preferencias)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferências atualizadas com sucesso!')
            return redirect('recommendation:profile')
    else:
        form = PreferencesForm(instance=user.preferencias)
    
    return render(request, 'recommendation/preferences_form.html', {
        'form': form,
        'user': user,
        'title': 'Editar Preferências',
        'button_text': 'Salvar'
    })
