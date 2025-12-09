from django.contrib import admin
from .models import User, Workout, Preferences, History


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'idade', 'peso', 'altura', 'objetivo', 'nivel', 'criado_em')
    list_filter = ('objetivo', 'nivel')
    search_fields = ('nome', 'email')
    ordering = ('-criado_em',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('nome', 'intensidade', 'duracao_minutos', 'calorias_estimadas', 'criado_em')
    list_filter = ('intensidade',)
    search_fields = ('nome', 'descricao')
    ordering = ('-criado_em',)


@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_treino_preferido', 'frequencia_treino_semana', 'horario_preferido')
    search_fields = ('usuario__nome',)


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'treino', 'criado_em')
    list_filter = ('data',)
    search_fields = ('usuario__nome',)
    ordering = ('-data',)
