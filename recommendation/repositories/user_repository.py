from typing import List, Optional
from ..models import User
from .base import BaseRepository


class UserRepository(BaseRepository):
    """Repositório para gerenciar operações de dados relacionadas a usuários.
    
    Implementa o padrão Repository para isolar a lógica de acesso a dados,
    fornecendo métodos específicos para busca de usuários por email, nível e objetivo.
    """
    
    def get_by_id(self, id: int) -> Optional[User]:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
    
    def get_all(self) -> List[User]:
        return list(User.objects.all())
    
    def save(self, entity: User) -> User:
        entity.save()
        return entity
    
    def update(self, entity: User) -> User:
        entity.save()
        return entity
    
    def delete(self, id: int) -> bool:
        try:
            user = User.objects.get(id=id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email.
        
        Args:
            email: Email do usuário.
            
        Returns:
            Usuário encontrado ou None se não existir.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    def find_by_nivel(self, nivel: str) -> List[User]:
        """Busca usuários por nível de experiência.
        
        Args:
            nivel: Nível de experiência (iniciante, intermediario, avancado).
            
        Returns:
            Lista de usuários com o nível especificado.
        """
        return list(User.objects.filter(nivel=nivel))
    
    def find_by_objetivo(self, objetivo: str) -> List[User]:
        """Busca usuários por objetivo.
        
        Args:
            objetivo: Objetivo do usuário (emagrecer, ganhar_massa, manter).
            
        Returns:
            Lista de usuários com o objetivo especificado.
        """
        return list(User.objects.filter(objetivo=objetivo))

