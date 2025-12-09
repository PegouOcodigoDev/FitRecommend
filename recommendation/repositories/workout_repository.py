from typing import List, Optional
from ..models import Workout
from .base import BaseRepository


class WorkoutRepository(BaseRepository):
    """Repositório para gerenciar operações de dados relacionadas a treinos.
    
    Implementa o padrão Repository para isolar a lógica de acesso a dados,
    fornecendo métodos específicos para busca de treinos por intensidade,
    duração e faixa de calorias.
    """
    
    def get_by_id(self, id: int) -> Optional[Workout]:
        try:
            return Workout.objects.get(id=id)
        except Workout.DoesNotExist:
            return None
    
    def get_all(self) -> List[Workout]:
        return list(Workout.objects.all())
    
    def save(self, entity: Workout) -> Workout:
        entity.save()
        return entity
    
    def update(self, entity: Workout) -> Workout:
        entity.save()
        return entity
    
    def delete(self, id: int) -> bool:
        try:
            workout = Workout.objects.get(id=id)
            workout.delete()
            return True
        except Workout.DoesNotExist:
            return False
    
    def find_by_intensidade(self, intensidade: str) -> List[Workout]:
        """Busca treinos por intensidade.
        
        Args:
            intensidade: Intensidade do treino (baixa, media, alta).
            
        Returns:
            Lista de treinos com a intensidade especificada.
        """
        return list(Workout.objects.filter(intensidade=intensidade))
    
    def find_by_duracao_max(self, duracao_max: int) -> List[Workout]:
        """Busca treinos com duração até um limite máximo.
        
        Args:
            duracao_max: Duração máxima em minutos.
            
        Returns:
            Lista de treinos com duração menor ou igual ao limite.
        """
        return list(Workout.objects.filter(duracao_minutos__lte=duracao_max))
    
    def find_by_calorias_range(self, min_cal: int, max_cal: int) -> List[Workout]:
        """Busca treinos por faixa de calorias.
        
        Args:
            min_cal: Calorias mínimas estimadas.
            max_cal: Calorias máximas estimadas.
            
        Returns:
            Lista de treinos dentro da faixa de calorias especificada.
        """
        return list(Workout.objects.filter(
            calorias_estimadas__gte=min_cal,
            calorias_estimadas__lte=max_cal
        ))

