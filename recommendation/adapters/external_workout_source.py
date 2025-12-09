from abc import ABC, abstractmethod
from typing import List
from ..models import Workout


class ExternalWorkoutSource(ABC):
    """Interface base para fontes externas de treinos.
    
    Define o contrato que todos os adapters de fontes externas devem seguir,
    permitindo integração com diferentes APIs de treinos.
    """
    
    @abstractmethod
    def fetch_workouts(self) -> List[Workout]:
        """Busca treinos de uma fonte externa.
        
        Returns:
            Lista de treinos convertidos para o formato interno.
        """
        pass
    
    def _get_fallback_workouts(self) -> List[Workout]:
        """Retorna treinos de fallback quando a fonte externa está indisponível.
        
        Returns:
            Lista de treinos padrão para uso quando a API externa falhar.
        """
        return []

