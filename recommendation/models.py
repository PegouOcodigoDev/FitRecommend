from django.db import models


class User(models.Model):
    """Modelo de usuário do sistema.
    
    Armazena informações pessoais, físicas e objetivos do usuário
    para personalização de recomendações de treinos.
    """
    OBJETIVO_CHOICES = [
        ('emagrecer', 'Emagrecer'),
        ('ganhar_massa', 'Ganhar Massa'),
        ('manter', 'Manter Forma'),
    ]
    
    NIVEL_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    idade = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.IntegerField()
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_CHOICES)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.nome} ({self.email})"


class Workout(models.Model):
    """Modelo de treino do sistema.
    
    Representa um treino ou exercício com informações sobre
    intensidade, duração e calorias estimadas.
    """
    INTENSIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    intensidade = models.CharField(max_length=20, choices=INTENSIDADE_CHOICES)
    duracao_minutos = models.IntegerField()
    calorias_estimadas = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'treinos'
        verbose_name = 'Treino'
        verbose_name_plural = 'Treinos'
    
    def __str__(self):
        return self.nome


class Preferences(models.Model):
    """Modelo de preferências de treino do usuário.
    
    Armazena preferências pessoais como frequência de treino,
    horário preferido e tipo de treino favorito.
    """
    TIPO_TREINO_CHOICES = [
        ('musculacao', 'Musculação'),
        ('cardio', 'Cardio'),
        ('hiit', 'HIIT'),
        ('yoga', 'Yoga'),
        ('crossfit', 'CrossFit'),
        ('funcional', 'Funcional'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferencias')
    frequencia_treino_semana = models.IntegerField(default=3)
    horario_preferido = models.CharField(max_length=50, blank=True)
    tipo_treino_preferido = models.CharField(max_length=50, choices=TIPO_TREINO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'preferencias'
        verbose_name = 'Preferência'
        verbose_name_plural = 'Preferências'
    
    def __str__(self):
        return f"Preferências de {self.usuario.nome}"


class History(models.Model):
    """Modelo de histórico de treinos do usuário.
    
    Registra treinos realizados pelo usuário em datas específicas,
    permitindo acompanhamento do progresso.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico')
    data = models.DateField()
    treino = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'historico'
        verbose_name = 'Histórico'
        verbose_name_plural = 'Históricos'
        ordering = ['-data']
    
    def __str__(self):
        return f"Histórico de {self.usuario.nome} - {self.data}"
