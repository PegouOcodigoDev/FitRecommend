from django.test import TestCase
from decimal import Decimal
from .models import User, Workout
from .repositories import UserRepository
from .strategies import (
    GoalBasedStrategy,
    BeginnerFriendlyStrategy,
    CalorieBasedStrategy,
    HybridStrategy
)
from .adapters import WgerWorkoutAdapter


class UserRepositoryTest(TestCase):
    """Testes para o UserRepository.
    
    Valida operações CRUD e métodos específicos de busca de usuários.
    """
    
    def setUp(self):
        self.repository = UserRepository()
        self.user_data = {
            'nome': 'Test User',
            'email': 'test@example.com',
            'idade': 25,
            'peso': Decimal('75.5'),
            'altura': 175,
            'objetivo': 'ganhar_massa',
            'nivel': 'iniciante'
        }
    
    def test_save_user(self):
        """Testa salvamento de novo usuário.
        
        Verifica se usuário é salvo corretamente com todos os campos.
        """
        user = User(**self.user_data)
        saved_user = self.repository.save(user)
        
        assert saved_user.id is not None
        assert saved_user.nome == 'Test User'
        assert saved_user.email == 'test@example.com'
    
    def test_get_by_id(self):
        """Testa busca de usuário por ID.
        
        Verifica se usuário é encontrado corretamente pelo ID.
        """
        user = User(**self.user_data)
        saved_user = self.repository.save(user)
        
        found_user = self.repository.get_by_id(saved_user.id)
        
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert found_user.nome == 'Test User'
    
    def test_get_by_email(self):
        """Testa busca de usuário por email.
        
        Verifica se usuário é encontrado corretamente pelo email.
        """
        user = User(**self.user_data)
        self.repository.save(user)
        
        found_user = self.repository.get_by_email('test@example.com')
        
        assert found_user is not None
        assert found_user.email == 'test@example.com'
    
    def test_find_by_nivel(self):
        """Testa busca de usuários por nível.
        
        Verifica se todos os usuários retornados possuem o nível especificado.
        """
        User.objects.create(**self.user_data)
        
        users = self.repository.find_by_nivel('iniciante')
        
        assert len(users) > 0
        assert all(u.nivel == 'iniciante' for u in users)
    
    def test_delete_user(self):
        """Testa remoção de usuário.
        
        Verifica se usuário é removido corretamente do banco de dados.
        """
        user = User(**self.user_data)
        saved_user = self.repository.save(user)
        
        result = self.repository.delete(saved_user.id)
        
        assert result is True
        assert self.repository.get_by_id(saved_user.id) is None


class GoalBasedStrategyTest(TestCase):
    """Testes para GoalBasedStrategy.
    
    Valida recomendações baseadas em objetivos do usuário.
    """
    
    def setUp(self):
        self.strategy = GoalBasedStrategy()
        
        self.user_emagrecer = User.objects.create(
            nome='User Emagrecer',
            email='emagrecer@test.com',
            idade=30,
            peso=Decimal('85.0'),
            altura=175,
            objetivo='emagrecer',
            nivel='intermediario'
        )
        
        self.workouts = [
            Workout.objects.create(
                nome='HIIT',
                descricao='Alta intensidade',
                intensidade='alta',
                duracao_minutos=30,
                calorias_estimadas=400
            ),
            Workout.objects.create(
                nome='Yoga',
                descricao='Baixa intensidade',
                intensidade='baixa',
                duracao_minutos=45,
                calorias_estimadas=150
            ),
        ]
    
    def test_recommend_for_weight_loss(self):
        """Testa recomendação para usuário com objetivo de emagrecer.
        
        Verifica se estratégia retorna treinos adequados para emagrecimento.
        """
        result = self.strategy.recommend(
            self.user_emagrecer,
            self.workouts
        )
        
        assert len(result.workouts) > 0
        assert 'emagrecimento' in result.reasoning.lower()


class BeginnerFriendlyStrategyTest(TestCase):
    """Testes para BeginnerFriendlyStrategy.
    
    Valida recomendações apropriadas para usuários iniciantes.
    """
    
    def setUp(self):
        self.strategy = BeginnerFriendlyStrategy()
        
        self.user = User.objects.create(
            nome='Iniciante',
            email='iniciante@test.com',
            idade=22,
            peso=Decimal('70.0'),
            altura=170,
            objetivo='manter',
            nivel='iniciante'
        )
        
        self.workouts = [
            Workout.objects.create(
                nome='Caminhada',
                descricao='Baixa intensidade',
                intensidade='baixa',
                duracao_minutos=30,
                calorias_estimadas=150
            ),
            Workout.objects.create(
                nome='CrossFit',
                descricao='Alta intensidade',
                intensidade='alta',
                duracao_minutos=60,
                calorias_estimadas=500
            ),
        ]
    
    def test_recommend_beginner_workouts(self):
        """Testa se recomenda treinos apropriados para iniciantes.
        
        Verifica se treinos recomendados são de baixa/média intensidade
        e com duração adequada para iniciantes.
        """
        result = self.strategy.recommend(self.user, self.workouts)
        
        assert len(result.workouts) > 0
        assert 'iniciante' in result.reasoning.lower()
        
        for workout in result.workouts:
            assert workout.intensidade in ['baixa', 'media']
            assert workout.duracao_minutos <= 45


class WgerWorkoutAdapterTest(TestCase):
    """Testes para WgerWorkoutAdapter.
    
    Valida integração com API Wger e conversão de dados para formato interno.
    """
    
    def setUp(self):
        self.adapter = WgerWorkoutAdapter()
    
    def test_fetch_workouts(self):
        """Testa busca e conversão de treinos da API Wger.
        
        Verifica se adapter retorna treinos válidos com todos os campos
        necessários e intensidade válida.
        """
        workouts = self.adapter.fetch_workouts()
        
        assert len(workouts) > 0
        
        for workout in workouts:
            assert hasattr(workout, 'nome')
            assert hasattr(workout, 'descricao')
            assert hasattr(workout, 'intensidade')
            assert hasattr(workout, 'duracao_minutos')
            assert hasattr(workout, 'calorias_estimadas')
            assert workout.intensidade in ['baixa', 'media', 'alta']


class CalorieBasedStrategyTest(TestCase):
    """Testes para CalorieBasedStrategy.
    
    Valida cálculos calóricos e recomendações baseadas em TMB.
    """
    
    def setUp(self):
        self.strategy = CalorieBasedStrategy()
        
        self.user = User.objects.create(
            nome='User Test',
            email='calorie@test.com',
            idade=30,
            peso=Decimal('80.0'),
            altura=180,
            objetivo='manter',
            nivel='intermediario'
        )
        
        self.workouts = [
            Workout.objects.create(
                nome='Treino',
                descricao='Teste',
                intensidade='media',
                duracao_minutos=40,
                calorias_estimadas=300
            ),
        ]
    
    def test_tmb_calculation(self):
        """Testa cálculo de TMB.
        
        Verifica se TMB é calculada corretamente e está em faixa razoável.
        """
        tmb = self.strategy._calcular_tmb(self.user)
        
        assert tmb > 0
        assert tmb > 1500
        assert tmb < 4000
    
    def test_caloric_goal_calculation(self):
        """Testa cálculo de meta calórica.
        
        Verifica se metas calóricas são ajustadas corretamente
        baseadas no objetivo do usuário.
        """
        tmb = 2000
        
        meta_emagrecer = self.strategy._calcular_meta_calorica(tmb, 'emagrecer')
        meta_ganhar = self.strategy._calcular_meta_calorica(tmb, 'ganhar_massa')
        meta_manter = self.strategy._calcular_meta_calorica(tmb, 'manter')
        
        assert meta_emagrecer < tmb
        assert meta_ganhar > tmb
        assert meta_manter == tmb
    
    def test_recommendation_includes_reasoning(self):
        """Testa se recomendação inclui justificativa.
        
        Verifica se resultado da recomendação contém reasoning
        explicando a escolha dos treinos.
        """
        result = self.strategy.recommend(self.user, self.workouts)
        
        assert result.reasoning is not None
        assert len(result.reasoning) > 0
        assert 'calórica' in result.reasoning.lower()


class HybridStrategyTest(TestCase):
    """Testes para HybridStrategy.
    
    Valida sistema de pontuação e combinação de múltiplos critérios.
    """
    
    def setUp(self):
        self.strategy = HybridStrategy()
        
        self.user = User.objects.create(
            nome='Hybrid User',
            email='hybrid@test.com',
            idade=28,
            peso=Decimal('75.0'),
            altura=175,
            objetivo='ganhar_massa',
            nivel='avancado'
        )
        
        self.workout = Workout.objects.create(
            nome='Musculação',
            descricao='Treino completo',
            intensidade='alta',
            duracao_minutos=60,
            calorias_estimadas=450
        )
    
    def test_workout_score_calculation(self):
        """Testa cálculo de score para treinos.
        
        Verifica se score é calculado corretamente e é um valor positivo.
        """
        score = self.strategy._calcular_score_workout(self.workout, self.user)
        
        assert score > 0
        assert isinstance(score, float)
    
    def test_recommendation_considers_multiple_factors(self):
        """Testa se recomendação considera múltiplos fatores.
        
        Verifica se reasoning menciona que múltiplos fatores foram considerados.
        """
        result = self.strategy.recommend(
            self.user,
            [self.workout]
        )
        
        assert 'híbrida' in result.reasoning.lower() or 'hybrid' in result.reasoning.lower()
        assert len(result.workouts) > 0
