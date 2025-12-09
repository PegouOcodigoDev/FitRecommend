from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from ..repositories import WorkoutRepository


@login_required
def workout_list(request):
    """Lista todos os treinos disponíveis.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do template workout_list.html com lista de treinos.
    """
    workout_repository = WorkoutRepository()
    workouts = workout_repository.get_all()
    
    return render(request, 'recommendation/workout_list.html', {
        'workouts': workouts
    })


@login_required
def workout_detail(request, workout_id):
    """Exibe detalhes de um treino específico.
    
    Args:
        request: Requisição HTTP do Django.
        workout_id: ID do treino a ser exibido.
        
    Returns:
        Renderização do template workout_detail.html ou página 404
        se treino não encontrado.
    """
    workout_repository = WorkoutRepository()
    workout = workout_repository.get_by_id(workout_id)
    
    if not workout:
        return render(request, '404.html', status=404)
    
    return render(request, 'recommendation/workout_detail.html', {
        'workout': workout
    })
