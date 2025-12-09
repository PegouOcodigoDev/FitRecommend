# 🎯 Objetivo
Projeto acadêmico desenvolvido para disciplina de Padrões Arquiteturais, demonstrando a aplicação prática de:
- Arquitetura MVC (adaptada ao Django)
- Repository Pattern
- Strategy Pattern  
- Adapter Pattern

## 🏗️ Arquitetura

### Padrões Implementados

- **MVC**: Arquitetura Model-View-Controller adaptada ao padrão Django (MTV)
- **Repository Pattern**: Camada de abstração para acesso a dados, isolando ORM
- **Strategy Pattern**: 4 algoritmos intercambiáveis de recomendação
- **Adapter Pattern**: Integração com APIs externas de formatos diferentes

### Tecnologias

- **Framework**: Django 5.x
- **Linguagem**: Python 3.11+
- **Banco de Dados**: SQLite
- **Containerização**: Docker
- **Gerenciador de Dependências**: Poetry
- **Testes**: Pytest + pytest-django

## 📋 Requisitos

- Python 3.11 ou superior
- Poetry
- Docker e Docker Compose (recomendado)

## ⚙️ Configuração

### API Externa Integrada

O sistema utiliza a **Wger Workout Manager API** (https://wger.de) para buscar treinos automaticamente:

- ✅ **Totalmente gratuita** - Não requer API key ou autenticação
- ✅ **Integração automática** - Busca treinos ao inicializar o sistema
- ✅ **Fallback inteligente** - Usa dados locais se a API estiver indisponível
- ✅ **Mais de 200 exercícios** disponíveis em múltiplas categorias

## 🚀 Instalação e Execução

### Opção 1: Com Docker (Recomendado)

```bash
# Build da imagem
docker-compose build

# Aplicar migrações do banco de dados
docker-compose run web python manage.py migrate

# Popular banco com dados de exemplo
docker-compose run web python manage.py seed_data

# Iniciar servidor
docker-compose up
```

### Opção 2: Sem Docker

```bash
# Instalar dependências
poetry install --no-root

# Aplicar migrações
poetry run python manage.py migrate

# Popular banco de dados
poetry run python manage.py seed_data

# Iniciar servidor
poetry run python manage.py runserver
```

## 🌐 Acesso ao Sistema

Após iniciar o servidor, acesse:

- **Dashboard Principal**: http://localhost:8000/
- **Login**: http://localhost:8000/login/
- **Registro**: http://localhost:8000/register/
- **Perfil**: http://localhost:8000/profile/
- **Lista de Treinos**: http://localhost:8000/workouts/
- **Histórico**: http://localhost:8000/history/
- **Admin Django**: http://localhost:8000/admin/

## 🧪 Testes

### Com Docker

```bash
docker-compose run web pytest
```

### Sem Docker

```bash
poetry run pytest
```

## 📁 Estrutura do Projeto

```
FitRecommend/
├── docs/                           # Documentação completa
│   └── adr_decisions.md           # Architecture Decision Records
├── recommendation/                 # App principal Django
│   ├── models.py                  # Models (Model do MVC)
│   ├── admin.py                   # Configuração do Django Admin
│   ├── urls.py                    # Rotas da aplicação
│   ├── forms.py                   # Formulários Django
│   ├── tests.py                   # Testes unitários
│   ├── repositories/              # Repository Pattern
│   │   ├── base.py               # Interface base
│   │   ├── user_repository.py
│   │   ├── workout_repository.py
│   │   └── history_repository.py
│   ├── strategies/                # Strategy Pattern
│   │   ├── base.py               # Interface Strategy
│   │   ├── calorie_based_strategy.py
│   │   ├── goal_based_strategy.py
│   │   ├── beginner_friendly_strategy.py
│   │   ├── hybrid_strategy.py
│   │   └── strategy_factory.py   # Factory para seleção
│   ├── adapters/                  # Adapter Pattern
│   │   ├── external_workout_source.py
│   │   └── wger_workout_adapter.py
│   ├── views/                     # Controllers (Controller do MVC)
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── recommendation_controller.py
│   │   ├── workout_controller.py
│   │   ├── history_controller.py
│   │   └── preferences_controller.py
│   ├── templates/                 # Views (View do MVC)
│   │   ├── base.html
│   │   ├── 404.html
│   │   └── recommendation/
│   │       ├── dashboard.html
│   │       ├── user_profile.html
│   │       ├── user_form.html
│   │       ├── workout_list.html
│   │       ├── workout_detail.html
│   │       ├── history.html
│   │       ├── history_form.html
│   │       ├── history_confirm_delete.html
│   │       ├── preferences_form.html
│   │       └── auth/
│   │           ├── login.html
│   │           ├── register.html
│   │           └── delete_account.html
│   └── management/commands/       # Comandos customizados
│       └── seed_data.py          # Popular banco de dados
├── workout_project/               # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml                 # Dependências Poetry
├── pytest.ini                     # Configuração pytest
├── manage.py
└── README.md
```

## 🎨 Funcionalidades

### 1. Dashboard de Recomendações

Cada usuário possui um dashboard personalizado que exibe:
- Recomendações de treinos baseadas em seu perfil
- Justificativa da recomendação
- Informações do perfil do usuário

### 2. Integração com API Externa Wger

O sistema integra com a API Wger Workout Manager (https://wger.de):
- Busca automática de exercícios da API Wger
- Conversão automática para formato interno usando Adapter Pattern
- Fallback inteligente com treinos padrão quando API está indisponível
- Mapeamento automático de categorias para intensidade
- Estimativa de duração e calorias baseada em categorias

Os treinos da API são integrados automaticamente ao inicializar o sistema
ou quando não há treinos locais disponíveis.

### 3. Sistema de Autenticação

- Registro de novos usuários
- Login e logout
- Exclusão de conta
- Proteção de rotas com autenticação obrigatória

### 4. Gerenciamento de Perfil

- Criação e edição de perfil de usuário
- Configuração de preferências de treino
- Visualização de perfil completo

### 5. Histórico de Treinos

- Registro completo de treinos realizados por cada usuário
- Visualização de histórico pessoal
- Estatísticas de treinos (total de sessões, minutos, calorias)
- Criação e exclusão de registros de histórico

## 📚 Documentação Completa

A pasta `/docs` contém documentação detalhada:

### architecture.md
- Visão geral da arquitetura MVC
- Explicação detalhada de cada padrão implementado
- Fluxos de execução
- Princípios SOLID aplicados
- Camadas da aplicação
- Pontos de extensão

### adr_decisions.md
- ADR-001: Strategy Pattern para Recomendações
- ADR-002: Adapter Pattern para APIs Externas
- ADR-003: Repository Pattern
- ADR-004: Django como Framework
- ADR-005: MVC Adaptado
- ADR-006: SQLite como Banco
- ADR-007: Strategy Factory

## 🔍 Rotas Principais

### Autenticação
- `GET/POST /register/` - Registro de novos usuários
- `GET/POST /login/` - Login de usuários
- `POST /logout/` - Logout
- `GET/POST /delete-account/` - Exclusão de conta

### Dashboard e Recomendações
- `GET /` - Dashboard principal com recomendações personalizadas

### Perfil e Preferências
- `GET /profile/` - Visualizar perfil do usuário
- `GET/POST /profile/setup/` - Configurar perfil inicial
- `GET/POST /profile/edit/` - Editar perfil
- `GET/POST /preferences/create/` - Criar preferências
- `GET/POST /preferences/edit/` - Editar preferências

### Treinos
- `GET /workouts/` - Lista todos os treinos disponíveis
- `GET /workouts/<id>/` - Detalhes de um treino específico

### Histórico
- `GET /history/` - Histórico de treinos do usuário
- `GET/POST /history/create/` - Adicionar registro ao histórico
- `GET/POST /history/<id>/delete/` - Excluir registro do histórico

## 👨‍💻 Autor

Eduardo Lima - eduardojunior010757@gmail.com

Para dúvidas sobre a arquitetura, consulte:
1. `/docs/adr_decisions.md` - Architecture Decision Records
2. Código fonte com docstrings padronizadas em português
3. README.md - Este arquivo