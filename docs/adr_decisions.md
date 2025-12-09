# Architecture Decision Records (ADRs)

Este documento registra as decisões arquiteturais importantes tomadas durante o desenvolvimento do sistema.

---

## ADR-001: Uso de Strategy Pattern para Recomendações

### Contexto

O sistema precisa gerar recomendações personalizadas de treinos para usuários com diferentes perfis, objetivos e níveis de experiência. Diferentes usuários requerem algoritmos de recomendação distintos.

### Decisão

Implementar o padrão **Strategy** para encapsular algoritmos de recomendação intercambiáveis.

### Estratégias Implementadas

1. **CalorieBasedStrategy**: Baseada em cálculos de TMB e metas calóricas
2. **GoalBasedStrategy**: Focada no objetivo específico do usuário
3. **BeginnerFriendlyStrategy**: Adaptada para usuários iniciantes
4. **HybridStrategy**: Combina múltiplos critérios com sistema de pontuação

### Justificativa

- **Flexibilidade**: Permite trocar algoritmos em tempo de execução
- **Open/Closed Principle**: Novas estratégias podem ser adicionadas sem modificar código existente
- **Testabilidade**: Cada estratégia pode ser testada isoladamente
- **Manutenibilidade**: Lógica de cada algoritmo fica isolada em sua própria classe
- **Single Responsibility**: Cada estratégia tem apenas uma responsabilidade

### Consequências

**Positivas**:
- Fácil adicionar novos algoritmos de recomendação
- Sistema mais modular e testável
- Permite personalização avançada

**Negativas**:
- Aumenta número de classes no sistema
- Pode ter overhead inicial de configuração

### Status

✅ **Aceito e Implementado**


## ADR-002: Uso de Adapter Pattern para Integração com APIs Externas

### Contexto

O sistema precisa integrar dados de APIs externas de treinos, cada uma com formato JSON diferente. Precisamos normalizar esses dados para o formato interno sem acoplar o sistema aos formatos externos.

### Decisão

Implementar o padrão **Adapter** para converter formatos externos em modelos internos.

### Adapters Implementados

**Para Treinos**:
- `ExternalWorkoutSource`: Interface base abstrata para fontes externas de treinos
- `WgerWorkoutAdapter`: Converte dados da API Wger (https://wger.de) → Workout interno

### Justificativa

- **Desacoplamento**: Sistema core não conhece formatos externos
- **Interoperabilidade**: Permite integrar múltiplas fontes heterogêneas
- **Isolamento de Mudanças**: Alterações em APIs externas afetam apenas adapters
- **Extensibilidade**: Fácil adicionar novos adapters para novas APIs
- **Single Responsibility**: Cada adapter só se preocupa com uma conversão específica

### Consequências

**Positivas**:
- Sistema independente de APIs externas
- Fácil trocar ou adicionar novas fontes de dados
- Testes não precisam de APIs reais (simulação)
- Mantém consistência de dados internos

**Negativas**:
- Aumenta número de classes
- Pode adicionar latência na conversão
- Necessita manutenção quando APIs externas mudam

### Status

✅ **Aceito e Implementado**


## ADR-003: Criação de Camada Repository Separada dos Models

### Contexto

O Django oferece ORM direto nos Models, mas isso pode levar a acoplamento forte entre controllers e camada de dados, dificultando testes e manutenção.

### Decisão

Implementar o padrão **Repository** como camada de abstração sobre o ORM do Django.

### Repositories Implementados

- `BaseRepository`: Interface base com operações CRUD
- `UserRepository`: Operações específicas de usuários
- `WorkoutRepository`: Operações específicas de treinos
- `HistoryRepository`: Operações específicas de histórico

### Justificativa

- **Separação de Responsabilidades**: Controllers não acessam ORM diretamente
- **Testabilidade**: Repositories podem ser mockados facilmente
- **Centralização**: Lógica de acesso a dados em um só lugar
- **Abstração**: Mudanças no ORM/banco afetam apenas repositories
- **Reusabilidade**: Mesmas queries podem ser reutilizadas

### Consequências

**Positivas**:
- Código mais limpo e organizado
- Testes mais simples (mock de repositories)
- Fácil trocar implementação de persistência
- Queries complexas centralizadas
- Melhor separação de camadas

**Negativas**:
- Mais código boilerplate
- Camada adicional pode parecer desnecessária para operações simples
- Curva de aprendizado para desenvolvedores acostumados com ORM direto

### Status

✅ **Aceito e Implementado**

---

## ADR-006: Uso de Django como Framework Base

### Contexto

Necessidade de escolher um framework web Python robusto para desenvolvimento rápido e com boas práticas estabelecidas.

### Decisão

Utilizar **Django** como framework web principal.

### Justificativa

- **Batteries Included**: ORM, admin, autenticação prontos
- **MTV/MVC**: Estrutura que facilita aplicação de padrões
- **Maturidade**: Framework estável e amplamente utilizado
- **Documentação**: Excelente documentação oficial
- **Comunidade**: Grande comunidade e ecossistema
- **Segurança**: Proteções built-in contra vulnerabilidades comuns
- **Produtividade**: Desenvolvimento rápido de protótipos e MVPs

### Alternativas Consideradas

- **Flask**: Mais leve mas requer mais configuração
- **FastAPI**: Excelente para APIs mas menos adequado para templates HTML

### Consequências

**Positivas**:
- Desenvolvimento rápido
- Admin panel gratuito
- ORM poderoso
- Sistema de templates robusto
- Middleware e segurança

**Negativas**:
- Pode ser "pesado" para projetos muito simples
- Estrutura opinionada (menos flexibilidade)
- Performance inferior a frameworks assíncronos em alguns casos

### Status

✅ **Aceito e Implementado**


## ADR-004: Arquitetura MVC Adaptada ao Django

### Contexto

Django nativamente usa padrão MTV (Model-Template-View), mas projeto requer aplicação explícita de MVC para fins acadêmicos.

### Decisão

Adaptar a estrutura do Django para seguir explicitamente o padrão **MVC**:

- **Model**: Models do Django
- **View**: Templates do Django
- **Controller**: Views do Django (organizadas como Controllers)

### Implementação

Views organizadas como classes Controller em diretório separado:
- `AuthController`: Autenticação e gerenciamento de sessão
- `UserController`: Gerenciamento de usuários
- `RecommendationController`: Geração de recomendações
- `WorkoutController`: Gerenciamento de treinos
- `HistoryController`: Histórico de treinos realizados
- `PreferencesController`: Preferências do usuário

### Justificativa

- **Clareza Acadêmica**: Explicita aplicação de MVC
- **Organização**: Controllers separados por responsabilidade
- **Manutenibilidade**: Lógica de controle isolada
- **Compatibilidade**: Mantém benefícios do Django
- **Documentação**: Facilita entendimento da arquitetura

### Consequências

**Positivas**:
- Arquitetura clara e bem documentada
- Fácil explicar e apresentar
- Organização lógica do código
- Separação de responsabilidades

**Negativas**:
- Pode confundir desenvolvedores Django tradicionais
- Camada adicional de abstração
- Documentação precisa explicar adaptação

### Status

✅ **Aceito e Implementado**


## ADR-005: Factory Pattern para Seleção de Estratégias

### Contexto

Com múltiplas estratégias de recomendação disponíveis, precisamos de mecanismo inteligente para selecionar a estratégia apropriada para cada usuário.

### Decisão

Implementar **RecommendationStrategyFactory** usando Factory Pattern.

### Regras de Seleção

```
- Usuário iniciante (nivel == 'iniciante') → BeginnerFriendlyStrategy
- Objetivo emagrecimento (objetivo == 'emagrecer') → GoalBasedStrategy
- Caso geral → HybridStrategy
```

A factory também oferece método `get_strategy_by_name()` para seleção manual por nome:
- `'calorie'` → CalorieBasedStrategy
- `'goal'` → GoalBasedStrategy
- `'beginner'` → BeginnerFriendlyStrategy
- `'hybrid'` → HybridStrategy

### Justificativa

- **Centralização**: Lógica de seleção em um só lugar
- **Flexibilidade**: Fácil ajustar regras de seleção
- **Open/Closed**: Adicionar estratégias não altera factory
- **Testabilidade**: Factory pode ser testada isoladamente
- **Encapsulamento**: Clientes não precisam conhecer todas as estratégias

### Consequências

**Positivas**:
- Seleção automática e inteligente
- Fácil customizar regras
- Controllers mais simples

**Negativas**:
- Camada adicional de abstração
- Regras hardcoded (poderia ser configurável)

### Status

✅ **Aceito e Implementado**