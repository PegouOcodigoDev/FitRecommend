from django.core.management.base import BaseCommand
from django.db import connection
from recommendation.models import Workout
from recommendation.adapters import WgerWorkoutAdapter


class Command(BaseCommand):
    """Comando de management para popular o banco de dados com dados de exemplo.
    
    Cria treinos locais com diferentes intensidades e integra dados
    da API Wger Workout Manager automaticamente.
    """
    help = 'Popula o banco de dados com dados de exemplo'
    
    def handle(self, *args, **options):
        self.stdout.write('🌱 Iniciando seed de dados...')
        
        if not self._check_tables_exist():
            self.stdout.write(self.style.ERROR('❌ Tabelas não existem. Execute "python manage.py migrate" primeiro.'))
            return
        
        self._clear_data()
        self._create_workouts()
        self._integrate_wger_workouts()
        
        total = Workout.objects.count()
        self.stdout.write(self.style.SUCCESS(f'✅ Seed concluído com sucesso! Total de {total} treinos no banco.'))
    
    def _check_tables_exist(self):
        table_names = connection.introspection.table_names()
        return 'treinos' in table_names
    
    def _clear_data(self):
        """Remove dados existentes para evitar duplicação.
        
        Limpa todos os treinos do banco de dados antes de popular
        com novos dados.
        """
        self.stdout.write('🗑️  Limpando dados existentes...')
        try:
            Workout.objects.all().delete()
        except Exception:
            pass
    
    def _create_workouts(self):
        """Cria treinos de exemplo com diferentes intensidades.
        
        Cria 8 treinos pré-definidos cobrindo baixa, média e alta
        intensidade para demonstração do sistema.
        """
        self.stdout.write('💪 Criando treinos...')
        
        workouts_data = [
            {
                'nome': 'Caminhada Leve',
                'descricao': 'Caminhada em ritmo moderado, ideal para iniciantes e aquecimento.',
                'intensidade': 'baixa',
                'duracao_minutos': 30,
                'calorias_estimadas': 150
            },
            {
                'nome': 'Corrida Moderada',
                'descricao': 'Corrida em ritmo constante para resistência cardiovascular.',
                'intensidade': 'media',
                'duracao_minutos': 40,
                'calorias_estimadas': 350
            },
            {
                'nome': 'HIIT Intenso',
                'descricao': 'Treino intervalado de alta intensidade para queima máxima de calorias.',
                'intensidade': 'alta',
                'duracao_minutos': 25,
                'calorias_estimadas': 400
            },
            {
                'nome': 'Musculação Completa',
                'descricao': 'Treino de musculação para corpo inteiro com foco em hipertrofia.',
                'intensidade': 'alta',
                'duracao_minutos': 60,
                'calorias_estimadas': 450
            },
            {
                'nome': 'Yoga Relaxante',
                'descricao': 'Sessão de yoga para flexibilidade, equilíbrio e relaxamento.',
                'intensidade': 'baixa',
                'duracao_minutos': 45,
                'calorias_estimadas': 120
            },
            {
                'nome': 'Ciclismo Indoor',
                'descricao': 'Pedalada indoor com variação de intensidade e resistência.',
                'intensidade': 'media',
                'duracao_minutos': 50,
                'calorias_estimadas': 380
            },
            {
                'nome': 'CrossFit Avançado',
                'descricao': 'WOD completo com levantamento de peso e exercícios funcionais.',
                'intensidade': 'alta',
                'duracao_minutos': 45,
                'calorias_estimadas': 500
            },
            {
                'nome': 'Natação Leve',
                'descricao': 'Natação em ritmo moderado para condicionamento geral.',
                'intensidade': 'media',
                'duracao_minutos': 35,
                'calorias_estimadas': 280
            },
        ]
        
        for data in workouts_data:
            Workout.objects.create(**data)
            self.stdout.write(f'  ✓ Treino criado: {data["nome"]}')
    
    def _integrate_wger_workouts(self):
        """Integra treinos da API Wger ao banco de dados.
        
        Busca exercícios da API Wger, converte para formato interno
        usando o adapter e adiciona ao banco, evitando duplicatas.
        """
        self.stdout.write('🌐 Buscando treinos da API Wger...')
        
        adapter = WgerWorkoutAdapter()
        try:
            wger_workouts = adapter.fetch_workouts()
            
            if not wger_workouts:
                self.stdout.write(self.style.WARNING('  ⚠️  Nenhum treino retornado da API Wger'))
                return
            
            added_count = 0
            skipped_count = 0
            
            for workout in wger_workouts:
                if not Workout.objects.filter(nome=workout.nome).exists():
                    workout.save()
                    added_count += 1
                    self.stdout.write(f'  ✓ Treino da API adicionado: {workout.nome}')
                else:
                    skipped_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'  ✅ Integração concluída: {added_count} novos treinos, {skipped_count} já existentes'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'  ❌ Erro ao integrar treinos da API Wger: {str(e)}')
            )
    