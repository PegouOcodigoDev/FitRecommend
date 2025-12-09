import requests
import logging
from typing import List
from .external_workout_source import ExternalWorkoutSource
from ..models import Workout

logger = logging.getLogger(__name__)


class WgerWorkoutAdapter(ExternalWorkoutSource):
    """Adapter para integração com a API Wger Workout Manager.
    
    Converte dados da API Wger (https://wger.de) para o formato interno
    de Workout, incluindo mapeamento de categorias para intensidade,
    estimativa de duração e calorias.
    """
    API_URL = "https://wger.de/api/v2"
    TIMEOUT = 15
    
    def fetch_workouts(self) -> List[Workout]:
        """Busca treinos da API Wger e converte para formato interno.
        
        Em caso de falha na API, retorna treinos de fallback.
        
        Returns:
            Lista de treinos convertidos da API Wger ou fallback.
        """
        try:
            workouts = []
            
            response = requests.get(
                f"{self.API_URL}/exerciseinfo/",
                params={
                    'limit': 20,
                    'language__code': 'pt'
                },
                timeout=self.TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                exercises = data.get('results', [])
                
                for exercise in exercises[:15]:
                    workout = self._convert_to_workout(exercise)
                    if workout:
                        workouts.append(workout)
            else:
                logger.warning(f"Wger API retornou status {response.status_code}")
            
            if not workouts:
                logger.info("Nenhum treino retornado da API Wger, usando fallback")
                return self._get_fallback_workouts()
            
            return workouts
            
        except requests.exceptions.Timeout:
            logger.error("Timeout ao conectar com Wger API")
            return self._get_fallback_workouts()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar treinos da Wger API: {str(e)}")
            return self._get_fallback_workouts()
        except Exception as e:
            logger.error(f"Erro inesperado no adapter Wger: {str(e)}")
            return self._get_fallback_workouts()
    
    def _convert_to_workout(self, api_data: dict) -> Workout:
        """Converte dados da API Wger para modelo Workout interno."""
        try:
            translations = api_data.get("translations", [])

            pt_translation = next((t for t in translations if t.get("language") == 7), None)

            en_translation = next((t for t in translations if t.get("language") == 2), None)

            translation = pt_translation or en_translation
            if not translation:
                return None

            name = translation.get("name", "").strip()
            if not name or len(name) < 3:
                return None

            description = translation.get("description", "")
            if description:
                tags = ["<p>", "</p>", "<ul>", "</ul>", "<li>", "</li>", "<b>", "</b>", "<em>", "</em>", "</ol>","<ol>"]
                for tag in tags:
                    description = description.replace(tag, " ")

                description = " ".join(description.split())
                if len(description) > 200:
                    description = description[:200] + "..."
            else:
                category = api_data.get("category", {})
                category_name = category.get("name", "Exercício") if isinstance(category, dict) else "Exercício"
                description = f"{category_name}: {name}"

            category = api_data.get("category", {})
            category_id = category.get("id", 0) if isinstance(category, dict) else category

            intensidade = self._map_category_to_intensity(category_id)
            duracao = self._estimate_duration(category_id, intensidade)
            calorias = self._estimate_calories(intensidade, duracao)

            workout = Workout(
                nome=name[:200],
                descricao=description[:500].strip(),
                intensidade=intensidade,
                duracao_minutos=duracao,
                calorias_estimadas=calorias,
            )

            return workout

        except Exception as e:
            logger.warning(f"Erro ao converter exercício: {str(e)}")
            return None

    
    def _map_category_to_intensity(self, category_id: int) -> str:
        """Mapeia ID de categoria da API para intensidade.
        
        Args:
            category_id: ID da categoria do exercício na API Wger.
            
        Returns:
            Intensidade mapeada (baixa, media, alta).
        """
        if category_id in [10, 8, 9]:
            return 'alta'
        elif category_id in [11, 12]:
            return 'baixa'
        else:
            return 'media'
    
    def _estimate_duration(self, category_id: int, intensidade: str) -> int:
        """Estima duração do treino baseada na categoria e intensidade.
        
        Args:
            category_id: ID da categoria do exercício.
            intensidade: Intensidade mapeada (baixa, media, alta).
            
        Returns:
            Duração estimada em minutos.
        """
        base_duration = 30
        
        if category_id in [10, 8]:
            base_duration = 45
        elif category_id in [11, 12, 13]:
            base_duration = 20
        
        if intensidade == 'alta':
            return min(base_duration + 15, 60)
        elif intensidade == 'baixa':
            return max(base_duration - 10, 15)
        
        return base_duration
    
    def _estimate_calories(self, intensidade: str, duration: int) -> int:
        """Estima calorias queimadas baseada na intensidade e duração.
        
        Args:
            intensidade: Intensidade do treino (baixa, media, alta).
            duration: Duração do treino em minutos.
            
        Returns:
            Calorias estimadas queimadas.
        """
        rates = {
            'baixa': 5,
            'media': 8,
            'alta': 12
        }
        
        rate = rates.get(intensidade, 8)
        return int(rate * duration)
    
    def _get_fallback_workouts(self) -> List[Workout]:
        """Retorna treinos de fallback quando a API está indisponível.
        
        Returns:
            Lista de treinos padrão para uso quando a API Wger falhar.
        """
        logger.info("Usando dados de fallback para treinos Wger")
        return [
            Workout(
                nome="Flexão de Braço",
                descricao="Exercício básico de força para peito e tríceps",
                intensidade='media',
                duracao_minutos=20,
                calorias_estimadas=160
            ),
            Workout(
                nome="Agachamento Livre",
                descricao="Exercício fundamental para pernas e glúteos",
                intensidade='media',
                duracao_minutos=25,
                calorias_estimadas=200
            ),
            Workout(
                nome="Prancha Abdominal",
                descricao="Exercício isométrico para core",
                intensidade='baixa',
                duracao_minutos=15,
                calorias_estimadas=75
            ),
            Workout(
                nome="Burpees",
                descricao="Exercício de corpo inteiro de alta intensidade",
                intensidade='alta',
                duracao_minutos=20,
                calorias_estimadas=240
            ),
            Workout(
                nome="Polichinelo",
                descricao="Exercício cardiovascular clássico",
                intensidade='media',
                duracao_minutos=15,
                calorias_estimadas=120
            ),
        ]

