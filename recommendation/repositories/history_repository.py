from typing import List, Optional
from datetime import date
from ..models import History, User
from .base import BaseRepository


class HistoryRepository(BaseRepository):
    """Repositório para gerenciar operações de dados relacionadas ao histórico.
    
    Implementa o padrão Repository para isolar a lógica de acesso a dados,
    fornecendo métodos específicos para busca de histórico por usuário,
    período e registros recentes.
    """
    
    def get_by_id(self, id: int) -> Optional[History]:
        try:
            return History.objects.get(id=id)
        except History.DoesNotExist:
            return None
    
    def get_all(self) -> List[History]:
        return list(History.objects.all())
    
    def save(self, entity: History) -> History:
        entity.save()
        return entity
    
    def update(self, entity: History) -> History:
        entity.save()
        return entity
    
    def delete(self, id: int) -> bool:
        try:
            history = History.objects.get(id=id)
            history.delete()
            return True
        except History.DoesNotExist:
            return False
    
    def find_by_user(self, user: User) -> List[History]:
        """Busca histórico de um usuário específico.
        
        Args:
            user: Usuário para buscar histórico.
            
        Returns:
            Lista de históricos ordenada por data (mais recente primeiro).
        """
        return list(History.objects.filter(usuario=user).order_by('-data'))
    
    def find_by_user_and_date_range(
        self, 
        user: User, 
        data_inicio: date, 
        data_fim: date
    ) -> List[History]:
        """Busca histórico de um usuário em um período específico.
        
        Args:
            user: Usuário para buscar histórico.
            data_inicio: Data inicial do período.
            data_fim: Data final do período.
            
        Returns:
            Lista de históricos no período ordenada por data (mais recente primeiro).
        """
        return list(History.objects.filter(
            usuario=user,
            data__gte=data_inicio,
            data__lte=data_fim
        ).order_by('-data'))
    
    def get_recent_by_user(self, user: User, limit: int = 10) -> List[History]:
        """Busca os registros mais recentes de um usuário.
        
        Args:
            user: Usuário para buscar histórico.
            limit: Número máximo de registros a retornar (padrão: 10).
            
        Returns:
            Lista dos registros mais recentes ordenada por data.
        """
        return list(History.objects.filter(usuario=user).order_by('-data')[:limit])

