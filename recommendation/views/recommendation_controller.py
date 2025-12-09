from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..repositories import UserRepository, WorkoutRepository, HistoryRepository
from ..adapters import WgerWorkoutAdapter
from ..models import Workout


@login_required
def dashboard(request):
    """Exibe dashboard personalizado com recomendações de treinos.
    
    Busca treinos da API Wger se não houver treinos locais e exibe
    recomendações baseadas no nível do usuário, além de estatísticas
    do histórico de treinos.
    
    Args:
        request: Requisição HTTP do Django.
        
    Returns:
        Renderização do template dashboard.html com dados do usuário,
        treinos recomendados e estatísticas.
    """
    user_repository = UserRepository()
    workout_repository = WorkoutRepository()
    history_repository = HistoryRepository()
    wger_adapter = WgerWorkoutAdapter()
    
    try:
        user = user_repository.get_by_email(request.user.email)
        if not user:
            return redirect('recommendation:profile_setup')
    except:
        return redirect('recommendation:profile_setup')
    
    all_workouts = workout_repository.get_all()
    if not all_workouts:
        fetched = wger_adapter.fetch_workouts()
        for workout in fetched:
            if not Workout.objects.filter(nome=workout.nome).exists():
                workout.save()
        all_workouts = workout_repository.get_all()
    history = history_repository.find_by_user(user)
    
    workouts_by_level = {
        'iniciante': [w for w in all_workouts if w.intensidade == 'baixa'],
        'intermediario': [w for w in all_workouts if w.intensidade == 'media'],
        'avancado': [w for w in all_workouts if w.intensidade == 'alta']
    }
    
    recommended_workouts = workouts_by_level.get(user.nivel, all_workouts)[:6]
    total_sessions = len(history)
    total_minutes = sum(item.treino.duracao_minutos for item in history if item.treino)
    total_calories = sum(item.treino.calorias_estimadas for item in history if item.treino)
    
    return render(request, 'recommendation/dashboard.html', {
        'user': user,
        'workouts': recommended_workouts,
        'all_workouts': all_workouts,
        'total_sessions': total_sessions,
        'total_minutes': total_minutes,
        'total_calories': total_calories
    })
