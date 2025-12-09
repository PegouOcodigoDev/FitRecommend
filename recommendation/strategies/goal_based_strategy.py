from typing import List
from .base import RecommendationStrategy, RecommendationResult


class GoalBasedStrategy(RecommendationStrategy):
    """Estratégia de recomendação baseada no objetivo do usuário.
    
    Seleciona treinos alinhados com o objetivo específico (emagrecer,
    ganhar massa ou manter forma).
    """
    
    def recommend(self, user, all_workouts: List) -> RecommendationResult:
        """Gera recomendações baseadas no objetivo do usuário.
        
        Args:
            user: Usuário para o qual gerar recomendações.
            all_workouts: Lista de todos os treinos disponíveis.
            
        Returns:
            Resultado contendo até 3 treinos recomendados e justificativa.
        """
        objetivo = user.objetivo
        
        workouts_recomendados = self._selecionar_treinos_por_objetivo(
            all_workouts, 
            objetivo
        )
        
        reasoning = self._gerar_justificativa(objetivo)
        
        return RecommendationResult(
            workouts=workouts_recomendados[:3],
            reasoning=reasoning
        )
    
    def _selecionar_treinos_por_objetivo(self, workouts: List, objetivo: str) -> List:
        """Seleciona treinos adequados ao objetivo.
        
        Args:
            workouts: Lista de treinos disponíveis.
            objetivo: Objetivo do usuário (emagrecer, ganhar_massa, manter).
            
        Returns:
            Lista de treinos recomendados ordenados por relevância.
        """
        if objetivo == 'emagrecer':
            treinos_filtrados = [
                w for w in workouts 
                if w.intensidade in ['media', 'alta'] and w.calorias_estimadas >= 250
            ]
            return sorted(treinos_filtrados, key=lambda w: -w.calorias_estimadas)
        
        elif objetivo == 'ganhar_massa':
            treinos_filtrados = [
                w for w in workouts 
                if w.intensidade in ['media', 'alta'] and w.duracao_minutos >= 30
            ]
            return sorted(treinos_filtrados, key=lambda w: -w.intensidade == 'alta')
        
        else:
            treinos_filtrados = [
                w for w in workouts 
                if w.intensidade == 'media'
            ]
            return treinos_filtrados
    
    def _gerar_justificativa(self, objetivo: str) -> str:
        """Gera justificativa da recomendação.
        
        Args:
            objetivo: Objetivo do usuário (emagrecer, ganhar_massa, manter).
            
        Returns:
            Texto explicativo da recomendação.
        """
        justificativas = {
            'emagrecer': (
                "Recomendação focada em emagrecimento: treinos de alta intensidade "
                "para queima calórica máxima."
            ),
            'ganhar_massa': (
                "Recomendação focada em ganho de massa muscular: treinos intensos "
                "com foco em resistência e hipertrofia."
            ),
            'manter': (
                "Recomendação focada em manutenção: treinos moderados "
                "para estabilidade corporal."
            ),
        }
        return justificativas.get(objetivo, "Recomendação baseada no objetivo do usuário.")

