from typing import List
from .base import RecommendationStrategy, RecommendationResult


class HybridStrategy(RecommendationStrategy):
    """Estratégia híbrida que combina múltiplos critérios.
    
    Considera meta calórica, objetivo, nível do usuário e preferências
    pessoais através de um sistema de pontuação.
    """
    
    def recommend(self, user, all_workouts: List) -> RecommendationResult:
        """Gera recomendações usando sistema híbrido de pontuação.
        
        Args:
            user: Usuário para o qual gerar recomendações.
            all_workouts: Lista de todos os treinos disponíveis.
            
        Returns:
            Resultado contendo até 3 treinos recomendados e justificativa
            explicando os fatores considerados.
        """
        score_workouts = []
        for workout in all_workouts:
            score = self._calcular_score_workout(workout, user)
            score_workouts.append((workout, score))
        
        score_workouts.sort(key=lambda x: -x[1])
        workouts_recomendados = [w for w, _ in score_workouts[:3]]
        
        reasoning = (
            f"Recomendação híbrida considerando múltiplos fatores: "
            f"nível ({user.nivel}), objetivo ({user.objetivo}), "
            f"meta calórica e preferências pessoais."
        )
        
        return RecommendationResult(
            workouts=workouts_recomendados,
            reasoning=reasoning
        )
    
    def _calcular_score_workout(self, workout, user) -> float:
        """Calcula score de adequação de um treino ao usuário.
        
        Considera nível de experiência, objetivo, calorias e preferências
        de frequência de treino.
        
        Args:
            workout: Treino a ser avaliado.
            user: Usuário com perfil e preferências.
            
        Returns:
            Score de adequação (maior valor indica melhor adequação).
        """
        score = 0.0
        
        if user.nivel == 'iniciante':
            if workout.intensidade == 'baixa':
                score += 3.0
            elif workout.intensidade == 'media':
                score += 1.5
        elif user.nivel == 'intermediario':
            if workout.intensidade == 'media':
                score += 3.0
            elif workout.intensidade in ['baixa', 'alta']:
                score += 1.5
        else:
            if workout.intensidade == 'alta':
                score += 3.0
            elif workout.intensidade == 'media':
                score += 1.5
        
        if user.objetivo == 'emagrecer':
            score += workout.calorias_estimadas / 100
        elif user.objetivo == 'ganhar_massa':
            if workout.intensidade == 'alta':
                score += 2.0
        
        if hasattr(user, 'preferencias'):
            if workout.duracao_minutos <= 30 and user.preferencias.frequencia_treino_semana >= 5:
                score += 1.0
            elif workout.duracao_minutos >= 45 and user.preferencias.frequencia_treino_semana <= 3:
                score += 1.0
        
        return score
    
    def _calcular_tmb(self, user) -> float:
        """Calcula Taxa Metabólica Basal.
        
        Args:
            user: Usuário com peso, altura e idade.
            
        Returns:
            TMB em kcal/dia ajustada por fator de atividade.
        """
        peso = float(user.peso)
        altura = user.altura
        idade = user.idade
        
        tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5
        return tmb * 1.55
    
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

