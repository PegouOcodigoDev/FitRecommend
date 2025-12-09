from typing import List
from .base import RecommendationStrategy, RecommendationResult


class BeginnerFriendlyStrategy(RecommendationStrategy):
    """Estratégia de recomendação para iniciantes.
    
    Prioriza treinos de baixa a média intensidade com durações moderadas,
    focando em adaptação gradual e construção de hábitos sustentáveis.
    """
    
    def recommend(self, user, all_workouts: List) -> RecommendationResult:
        """Gera recomendações apropriadas para usuários iniciantes.
        
        Args:
            user: Usuário para o qual gerar recomendações.
            all_workouts: Lista de todos os treinos disponíveis.
            
        Returns:
            Resultado contendo até 3 treinos recomendados e justificativa.
        """
        workouts_recomendados = self._selecionar_treinos_iniciantes(all_workouts)
        
        reasoning = (
            "Recomendação para iniciantes: treinos de baixa a média intensidade "
            "com durações moderadas. Foco em adaptação gradual e construção de hábitos sustentáveis."
        )
        
        return RecommendationResult(
            workouts=workouts_recomendados[:3],
            reasoning=reasoning
        )
    
    def _selecionar_treinos_iniciantes(self, workouts: List) -> List:
        """Seleciona treinos adequados para iniciantes.
        
        Args:
            workouts: Lista de treinos disponíveis.
            
        Returns:
            Lista de treinos para iniciantes ordenados por adequação.
        """
        treinos_filtrados = [
            w for w in workouts 
            if w.intensidade in ['baixa', 'media'] and w.duracao_minutos <= 45
        ]
        
        return sorted(
            treinos_filtrados,
            key=lambda w: (w.intensidade == 'baixa', -w.duracao_minutos),
            reverse=True
        )

