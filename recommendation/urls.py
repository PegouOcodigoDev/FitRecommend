from django.urls import path
from .views import (
    auth_controller,
    user_controller,
    recommendation_controller,
    workout_controller,
    history_controller,
    preferences_controller
)

app_name = 'recommendation'

urlpatterns = [
    path('register/', auth_controller.register_view, name='register'),
    path('login/', auth_controller.login_view, name='login'),
    path('logout/', auth_controller.logout_view, name='logout'),
    path('delete-account/', auth_controller.delete_account_view, name='delete_account'),
    
    path('', recommendation_controller.dashboard, name='home'),
    
    path('profile/', user_controller.user_profile, name='profile'),
    path('profile/setup/', user_controller.user_setup, name='profile_setup'),
    path('profile/edit/', user_controller.user_edit, name='profile_edit'),
    
    path('preferences/edit/', preferences_controller.preferences_edit, name='preferences_edit'),
    path('preferences/create/', preferences_controller.preferences_create, name='preferences_create'),
    
    path('workouts/', workout_controller.workout_list, name='workout_list'),
    path('workouts/<int:workout_id>/', workout_controller.workout_detail, name='workout_detail'),
    
    path('history/', history_controller.user_history, name='history'),
    path('history/create/', history_controller.history_create, name='history_create'),
    path('history/<int:history_id>/delete/', history_controller.history_delete, name='history_delete'),
]
