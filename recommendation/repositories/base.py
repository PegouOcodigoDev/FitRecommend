from abc import ABC, abstractmethod
from typing import List, Optional, Any


class BaseRepository(ABC):
    """Interface base para todos os repositórios.
    
    Define operações CRUD padrão que devem ser implementadas por todos
    os repositórios do sistema.
    """
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Any]:
        """Busca uma entidade por ID.
        
        Args:
            id: Identificador único da entidade.
            
        Returns:
            Entidade encontrada ou None se não existir.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        """Retorna todas as entidades.
        
        Returns:
            Lista de todas as entidades do tipo.
        """
        pass
    
    @abstractmethod
    def save(self, entity: Any) -> Any:
        """Salva uma nova entidade.
        
        Args:
            entity: Entidade a ser salva.
            
        Returns:
            Entidade salva com ID atribuído.
        """
        pass
    
    @abstractmethod
    def update(self, entity: Any) -> Any:
        """Atualiza uma entidade existente.
        
        Args:
            entity: Entidade a ser atualizada.
            
        Returns:
            Entidade atualizada.
        """
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Remove uma entidade.
        
        Args:
            id: Identificador da entidade a ser removida.
            
        Returns:
            True se removida com sucesso, False caso contrário.
        """
        pass

