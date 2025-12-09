from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from ..repositories import HistoryRepository, UserRepository
from ..forms import HistoryForm


@login_required
def user_history(request):
    """Exibe histórico de treinos do usuário autenticado.
    
    Args:
        request: Requisição HTTP do Django com parâmetro opcional 'limit'.
        
    Returns:
        Renderização do template history.html com histórico e estatísticas
        ou redirecionamento se perfil não configurado.
    """
    user_repository = UserRepository()
    history_repository = HistoryRepository()
    
    user = user_repository.get_by_email(request.user.email)
    if not user:
        return redirect('recommendation:profile_setup')
    
    limit = int(request.GET.get('limit', 20))
    history = history_repository.get_recent_by_user(user, limit)
    
    total_minutos = sum(
        item.treino.duracao_minutos 
        for item in history 
        if item.treino
    )
    
    return render(request, 'recommendation/history.html', {
        'user': user,
        'history': history,
        'total_minutos': total_minutos
    })


@login_required
def history_create(request):
    """Cria novo registro no histórico de treinos.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do formulário de criação ou redirecionamento
        após salvamento bem-sucedido.
    """
    user_repository = UserRepository()
    user = user_repository.get_by_email(request.user.email)
    
    if not user:
        return redirect('recommendation:profile_setup')
    
    if request.method == 'POST':
        form = HistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.usuario = user
            history.save()
            messages.success(request, 'Registro adicionado ao histórico!')
            return redirect('recommendation:history')
    else:
        form = HistoryForm(initial={'usuario': user.id})
    
    return render(request, 'recommendation/history_form.html', {
        'form': form,
        'title': 'Adicionar ao Histórico',
        'button_text': 'Adicionar'
    })


@login_required
def history_delete(request, history_id):
    """Remove registro do histórico de treinos.
    
    Args:
        request: Requisição HTTP do Django.
        history_id: ID do registro a ser removido.
        
    Returns:
        Renderização da página de confirmação ou redirecionamento
        após exclusão bem-sucedida.
    """
    history_repository = HistoryRepository()
    user_repository = UserRepository()
    
    user = user_repository.get_by_email(request.user.email)
    if not user:
        return redirect('recommendation:profile_setup')
    
    history = history_repository.get_by_id(history_id)
    
    if not history or history.usuario.id != user.id:
        return render(request, '404.html', status=404)
    
    if request.method == 'POST':
        history.delete()
        messages.success(request, 'Registro excluído do histórico!')
        return redirect('recommendation:history')
    
    return render(request, 'recommendation/history_confirm_delete.html', {
        'history': history
    })
