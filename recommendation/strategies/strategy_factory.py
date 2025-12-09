from .base import RecommendationStrategy
from .calorie_based_strategy import CalorieBasedStrategy
from .goal_based_strategy import GoalBasedStrategy
from .beginner_friendly_strategy import BeginnerFriendlyStrategy
from .hybrid_strategy import HybridStrategy


class RecommendationStrategyFactory:
    """Factory para selecionar a estratégia de recomendação apropriada.
    
    Implementa lógica de decisão baseada nas características do usuário,
    selecionando automaticamente a melhor estratégia para cada perfil.
    """
    
    @staticmethod
    def get_strategy_for_user(user) -> RecommendationStrategy:
        """Seleciona estratégia apropriada baseada no perfil do usuário.
        
        Regras de seleção:
        - Usuário iniciante → BeginnerFriendlyStrategy
        - Objetivo emagrecimento → GoalBasedStrategy
        - Caso geral → HybridStrategy
        
        Args:
            user: Usuário com perfil e características.
            
        Returns:
            Instância da estratégia selecionada.
        """
        if user.nivel == 'iniciante':
            return BeginnerFriendlyStrategy()
        
        if user.objetivo == 'emagrecer':
            return GoalBasedStrategy()
        
        return HybridStrategy()
    
    @staticmethod
    def get_strategy_by_name(strategy_name: str) -> RecommendationStrategy:
        """Retorna uma estratégia específica pelo nome.
        
        Args:
            strategy_name: Nome da estratégia (calorie, goal, beginner, hybrid).
            
        Returns:
            Instância da estratégia solicitada.
            
        Raises:
            ValueError: Se o nome da estratégia for inválido.
        """
        strategies = {
            'calorie': CalorieBasedStrategy(),
            'goal': GoalBasedStrategy(),
            'beginner': BeginnerFriendlyStrategy(),
            'hybrid': HybridStrategy(),
        }
        
        strategy = strategies.get(strategy_name.lower())
        if not strategy:
            raise ValueError(f"Estratégia '{strategy_name}' não encontrada")
        
        return strategy

