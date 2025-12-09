from django import forms
from .models import User, Workout, Preferences, History


class UserForm(forms.ModelForm):
    """Formulário para criação e edição de usuários.
    
    Permite configurar nome, email, idade, peso, altura, objetivo e nível
    de experiência do usuário.
    """
    class Meta:
        model = User
        fields = ['nome', 'email', 'idade', 'peso', 'altura', 'objetivo', 'nivel']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Idade'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso em kg', 'step': '0.01'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Altura em cm'}),
            'objetivo': forms.Select(attrs={'class': 'form-select'}),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'idade': 'Idade',
            'peso': 'Peso (kg)',
            'altura': 'Altura (cm)',
            'objetivo': 'Objetivo',
            'nivel': 'Nível',
        }


class WorkoutForm(forms.ModelForm):
    """Formulário para criação e edição de treinos.
    
    Permite configurar nome, descrição, intensidade, duração e calorias
    estimadas de um treino.
    """
    class Meta:
        model = Workout
        fields = ['nome', 'descricao', 'intensidade', 'duracao_minutos', 'calorias_estimadas']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do treino'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada'}),
            'intensidade': forms.Select(attrs={'class': 'form-select'}),
            'duracao_minutos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duração em minutos'}),
            'calorias_estimadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calorias estimadas'}),
        }
        labels = {
            'nome': 'Nome do Treino',
            'descricao': 'Descrição',
            'intensidade': 'Intensidade',
            'duracao_minutos': 'Duração (minutos)',
            'calorias_estimadas': 'Calorias Estimadas',
        }


class PreferencesForm(forms.ModelForm):
    """Formulário para criação e edição de preferências de treino.
    
    Permite configurar frequência semanal, horário preferido e tipo
    de treino favorito do usuário.
    """
    class Meta:
        model = Preferences
        fields = ['frequencia_treino_semana', 'horario_preferido', 'tipo_treino_preferido']
        widgets = {
            'frequencia_treino_semana': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de treinos por semana', 'min': '1', 'max': '7'}),
            'horario_preferido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: manhã, tarde, noite'}),
            'tipo_treino_preferido': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'frequencia_treino_semana': 'Frequência Semanal',
            'horario_preferido': 'Horário Preferido',
            'tipo_treino_preferido': 'Tipo de Treino Preferido',
        }


class HistoryForm(forms.ModelForm):
    """Formulário para criação de registros de histórico.
    
    Permite registrar treinos realizados pelo usuário em datas específicas
    com observações opcionais.
    """
    class Meta:
        model = History
        fields = ['usuario', 'data', 'treino', 'observacoes']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'treino': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais (opcional)'}),
        }
        labels = {
            'usuario': 'Usuário',
            'data': 'Data',
            'treino': 'Treino',
            'observacoes': 'Observações',
        }
