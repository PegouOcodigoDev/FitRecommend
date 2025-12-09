from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class RecommendationResult:
    """Resultado de uma recomendação contendo treinos sugeridos.
    
    Attributes:
        workouts: Lista de treinos recomendados.
        reasoning: Justificativa da recomendação.
    """
    workouts: List[any]
    reasoning: str


class RecommendationStrategy(ABC):
    """Interface para estratégias de recomendação.
    
    Define o contrato que todas as estratégias devem seguir.
    """
    
    @abstractmethod
    def recommend(
        self, 
        user: any, 
        all_workouts: List[any]
    ) -> RecommendationResult:
        """Gera recomendações personalizadas para um usuário.
        
        Args:
            user: Usuário para o qual gerar recomendações.
            all_workouts: Lista de todos os treinos disponíveis.
            
        Returns:
            Resultado contendo treinos recomendados e justificativa.
        """
        pass

