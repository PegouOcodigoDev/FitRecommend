from typing import List
from .base import RecommendationStrategy, RecommendationResult


class CalorieBasedStrategy(RecommendationStrategy):
    """Estratégia de recomendação baseada em metas calóricas.
    
    Calcula a Taxa Metabólica Basal (TMB) do usuário e prioriza treinos
    que ajudam a atingir a meta calórica diária baseada no objetivo.
    """
    
    def recommend(self, user, all_workouts: List) -> RecommendationResult:
        """Gera recomendações baseadas em metas calóricas.
        
        Args:
            user: Usuário para o qual gerar recomendações.
            all_workouts: Lista de todos os treinos disponíveis.
            
        Returns:
            Resultado contendo até 3 treinos recomendados e justificativa
            com informações calóricas.
        """
        tmb = self._calcular_tmb(user)
        meta_calorica = self._calcular_meta_calorica(tmb, user.objetivo)
        
        workouts_recomendados = self._selecionar_treinos_por_calorias(
            all_workouts, 
            meta_calorica
        )
        
        reasoning = (
            f"Recomendação baseada em meta calórica de {meta_calorica:.0f} kcal/dia. "
            f"TMB calculada: {tmb:.0f} kcal/dia. Objetivo: {user.objetivo}."
        )
        
        return RecommendationResult(
            workouts=workouts_recomendados[:3],
            reasoning=reasoning
        )
    
    def _calcular_tmb(self, user) -> float:
        """Calcula Taxa Metabólica Basal usando equação de Mifflin-St Jeor.
        
        Args:
            user: Usuário com peso, altura e idade.
            
        Returns:
            TMB em kcal/dia ajustada por fator de atividade.
        """
        peso = float(user.peso)
        altura = user.altura
        idade = user.idade
        
        tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5
        
        fator_atividade = 1.55
        return tmb * fator_atividade
    
    def _calcular_meta_calorica(self, tmb: float, objetivo: str) -> float:
        """Calcula meta calórica baseada no objetivo.
        
        Args:
            tmb: Taxa metabólica basal em kcal/dia.
            objetivo: Objetivo do usuário (emagrecer, ganhar_massa, manter).
            
        Returns:
            Meta calórica diária ajustada ao objetivo.
        """
        if objetivo == 'emagrecer':
            return tmb * 0.8
        elif objetivo == 'ganhar_massa':
            return tmb * 1.15
        else:
            return tmb
    
    def _selecionar_treinos_por_calorias(
        self, 
        workouts: List, 
        meta_calorica: float
    ) -> List:
        """Seleciona treinos baseados na meta calórica.
        
        Args:
            workouts: Lista de treinos disponíveis.
            meta_calorica: Meta calórica do usuário em kcal/dia.
            
        Returns:
            Lista de treinos ordenados por proximidade à meta calórica.
        """
        treinos_ordenados = sorted(
            workouts,
            key=lambda w: abs(w.calorias_estimadas - (meta_calorica * 0.2))
        )
        return treinos_ordenados

